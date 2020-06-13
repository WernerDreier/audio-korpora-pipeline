import concurrent
import os
import re
import shutil
import xml.etree.ElementTree as ET  # TODO do we have this as requirement?
from concurrent.futures import as_completed
from concurrent.futures._base import as_completed
from pathlib import Path

import ffmpeg
import pandas as pd
import webrtcvad

from audio_korpora_pipeline.baseobjects import FileHandlingObject
from audio_korpora_pipeline.inputadapter.audiosplit.splitter import Splitter
from audio_korpora_pipeline.metamodel.mediasession import MediaAnnotationBundle, \
  MediaAnnotationBundleWithoutTranscription, WrittenResource, MediaFile, \
  MediaSessionActor, Sex, \
  MediaSessionActors, MediaSession


class Adapter(FileHandlingObject):
  def __init__(self, config):
    super(Adapter, self).__init__()

  def toMetamodel(self) -> MediaSession:
    raise NotImplementedError("Please use a subclass")

  def skipAlreadyProcessedFiles(self):
    skip = self.config['global']['skipAlreadyProcessedFiles']
    if not (skip):
      self.logger.warn("No config setting for skipAlreadyProcessedFiles set. Assuming True")
      return True
    return skip


class UntranscribedMediaSplittingAdapter(Adapter):
  AUDIO_SPLIT_AGRESSIVENESS = 3  # webrtcvad 1 (low), 3 (max)
  ADAPTERNAME = "MediaSplittingAdapter"
  mediaAnnotationBundles = []
  mediaSessionActors = set()  # using a set so we don't have duplets

  def __init__(self, config):
    super(UntranscribedMediaSplittingAdapter, self).__init__(config=config)
    self.config = config
    self.mediaSessionActors.add(MediaSessionActor("UNKNOWN", Sex.UNKNOWN, None))

  def _splitMonoRawAudioToVoiceSectionsThread(self, file, outputpath):
    self.logger.debug("Splitting file into chunks: {}".format(self._getFilenameWithExtension(file)))
    splitter = Splitter()
    vad = webrtcvad.Vad(int(self.AUDIO_SPLIT_AGRESSIVENESS))
    basename = self._getFilenameWithoutExtension(file)
    audiochunkPathsForThisfile = []
    try:
      audio, sample_rate = splitter.read_wave(file)
      frames = splitter.frame_generator(30, audio, sample_rate)
      frames = list(frames)
      segments = splitter.vad_collector(sample_rate, 30, 300, vad, frames)
      for i, segment in enumerate(segments):
        path = os.path.join(outputpath, basename + '_chunk_{:05d}.wav'.format(i))
        self.logger.debug("Write chunk {} of file {}".format(i, file))
        splitter.write_wave(path, segment, sample_rate)
        audiochunkPathsForThisfile.append(path)
      # write staging complete file
      stagingPath = os.path.join(outputpath, basename + ".stagingComplete")
      with open(stagingPath, 'a'):
        os.utime(stagingPath, None)
      self.logger.debug("Finished splitting file {}".format(file))
    except Exception as excep:
      self.logger.warn("Could split file into chunks {}. Skipping".format(file), exc_info=excep)
      return (False, str(file), [])  # returning an empty list, as no success here
    return (True, str(file), audiochunkPathsForThisfile)

  def _convertMediafileToMonoAudioThread(self, filenumber, totalNumberOfFiles, singleFilepathToProcess, outputPath):
    self.logger.debug(
        "Processing file {}/{} on path {}".format(filenumber + 1, totalNumberOfFiles, singleFilepathToProcess))
    nextFilename = os.path.join(outputPath, self._getFilenameWithoutExtension(singleFilepathToProcess) + ".wav")
    try:
      (ffmpeg
       .input(singleFilepathToProcess)
       .output(nextFilename, format='wav', acodec='pcm_s16le', ac=1, ar='16k')
       .overwrite_output()
       .run()
       )
    except ffmpeg.Error as ffmpgError:
      self.logger.warn("Ffmpeg rose an error", exc_info=ffmpgError)
      self.logger.warn("Due to error of ffmpeg skipped file {}".format(singleFilepathToProcess))
      return (False, str(singleFilepathToProcess), str(nextFilename))
    except Exception as e:
      self.logger.warn("Got an error while using ffmpeg for file {}".format(singleFilepathToProcess), exc_info=e)
      return (False, str(singleFilepathToProcess), str(nextFilename))
    return (True, str(singleFilepathToProcess), str(nextFilename))

  def createMediaSession(self, bundles):
    session = MediaSession(self.ADAPTERNAME, self.mediaSessionActors, bundles)
    return session

  def createMediaAnnotationBundles(self, audiochunks):
    annotationBundles = []
    for index, filepath in enumerate(audiochunks):
      bundle = MediaAnnotationBundleWithoutTranscription(identifier=filepath)  # we do not have any written ressources
      bundle.setMediaFile(filepath)
      annotationBundles.append(bundle)
    return annotationBundles

  def splitAudioToChunks(self, filesToChunk, outputPath):
    if ((filesToChunk == None) or (len(filesToChunk) == 0)):
      self.logger.info("Nothing to split, received empty wav-filenamelist")
      return []

    successfullyChunkedFiles = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
      futures = []
      for filenumber, file in enumerate(filesToChunk):
        futures.append(
            executor.submit(self._splitMonoRawAudioToVoiceSectionsThread, file, outputPath))
    for future in as_completed(futures):
      if (future.result()[0] == False):
        self.logger.warning("Couldnt split audiofile {}, removing from list".format(future.result()[1]))
      else:
        successfullyChunkedFiles.extend(future.result()[2])
      self.logger.debug("Splitting Audio is done {}".format(future.result()))
    self.logger.debug("Finished splitting {} wav files".format(len(filesToChunk)))
    return successfullyChunkedFiles

  def determineWavFilesToChunk(self, baseFilesToChunk, stagingChunkPath):
    allStageIndicatorFilesFullpath = set(self._getAllMediaFilesInBasepath(stagingChunkPath, {".stagingComplete"}))
    allExistingChunkedFilesFullpath = set(self._getAllMediaFilesInBasepath(stagingChunkPath, {".wav"}))

    allStageIndicatorFilesDictionary = self._toFilenameDictionary(allStageIndicatorFilesFullpath)
    allBaseFilesDictionary = self._toFilenameDictionary(baseFilesToChunk)

    stagingCompleteCorrectKeys = set(allBaseFilesDictionary.keys()).intersection(
        set(allStageIndicatorFilesDictionary.keys()))
    stagingIncompleteCorrectKeys = set(allBaseFilesDictionary.keys()).difference(
        set(allStageIndicatorFilesDictionary.keys()))

    stagingComplete = []
    for fullpath in allExistingChunkedFilesFullpath:
      if any(self._getFilenameWithoutExtension(fullpath).startswith(cm) for cm in stagingCompleteCorrectKeys):
        stagingComplete.append(fullpath)

    stagingIncomplete = [allBaseFilesDictionary[key] for key in stagingIncompleteCorrectKeys]

    self.logger.debug("Got {} files not yet chunked".format(len(stagingIncomplete)))
    self.logger.debug("Got {} files chunked".format(len(stagingComplete)))
    return stagingIncomplete, stagingComplete

  def convertMediaFilesToMonoAudio(self, filesToProcess, outputpath, adapterName):
    if (filesToProcess == None or len(filesToProcess) == 0):
      self.logger.debug("No files to convert for {}, skipping".format(adapterName))
      return []

    successfulFilenames = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
      futures = []
      for filenumber, currentFile in enumerate(filesToProcess):
        futures.append(
            executor.submit(self._convertMediafileToMonoAudioThread, filenumber, len(filesToProcess),
                            currentFile, outputpath))
    for future in as_completed(futures):
      if (future.result()[0] == False):
        self.logger.warning("Couldnt process audiofile {}, removing from list".format(future.result()[1]))
      else:
        successfulFilenames.append(future.result()[2])
      self.logger.debug("Processing Audio is done {} for Converter {}".format(future.result(), adapterName))

    return successfulFilenames

  def _toFilenameDictionary(self, list):
    if (list == None or len(list) == 0):
      self.logger.debug("Got nothing in list, returning empty dictionary")
      return dict()
    listDict = dict()
    for fullpath in list:
      listDict[self._getFilenameWithoutExtension(fullpath)] = fullpath
    self.logger.debug("Created dictionary of files of length {}".format(len(listDict)))
    return listDict

  def determineFilesToConvertToMonoFromGivenLists(self, alreadyStagedFiles, originalFiles, adaptername):
    dictionaryOfOriginalFilepaths = self._toFilenameDictionary(originalFiles)
    dictionaryOfStagedFilepaths = self._toFilenameDictionary(alreadyStagedFiles)

    notYetProcessedKeys = set(dictionaryOfOriginalFilepaths.keys()).difference(set(dictionaryOfStagedFilepaths.keys()))
    alreadyProcessedKeys = set(dictionaryOfOriginalFilepaths.keys()).intersection(
        set(dictionaryOfStagedFilepaths.keys()))

    fullpathsToNotYetProcessed = [dictionaryOfOriginalFilepaths[key] for key in notYetProcessedKeys]
    fullpathsProcessed = [dictionaryOfStagedFilepaths[key] for key in alreadyProcessedKeys]

    self.logger.debug("Got {} files not yet processed for corpus {}".format(len(notYetProcessedKeys), adaptername))
    self.logger.debug("Got {} files already processed for corpus {}".format(len(alreadyProcessedKeys), adaptername))
    return fullpathsToNotYetProcessed, fullpathsProcessed

  def _preprocess_workflow_with_splitting(self, filesAlreadyProcessed, filesToProcess, monoPath, chunkPath,
      adaptername):
    filesSuccessfullyProcessed = self.convertMediaFilesToMonoAudio(filesToProcess, monoPath, adaptername)
    baseFilesToChunk = []
    baseFilesToChunk = baseFilesToChunk + filesSuccessfullyProcessed + filesAlreadyProcessed
    # split mono audio to chunks
    filesToChunk, filesAlreadyChunked = self.determineWavFilesToChunk(baseFilesToChunk,
                                                                      chunkPath)
    filesSuccessfullyChunked = self.splitAudioToChunks(filesToChunk, chunkPath)
    # add chunks to media session
    mediaBundleFiles = [] + filesSuccessfullyChunked + filesAlreadyChunked
    mediaAnnotationbundles = self.createMediaAnnotationBundles(mediaBundleFiles)
    mediaSession = self.createMediaSession(mediaAnnotationbundles)
    return mediaSession


class UntranscribedVideoAdapter(UntranscribedMediaSplittingAdapter):
  ADAPTERNAME = "UntranscribedVideoAdapter"

  def __init__(self, config):
    super(UntranscribedVideoAdapter, self).__init__(config=config)
    self.config = config

  def toMetamodel(self):
    self.logger.debug("Untranscribed Video Korpus")
    # convert video to mono audio
    filesToProcess, filesAlreadyProcessed = self._determineVideoFilesToConvertToMono()
    return self._preprocess_workflow_with_splitting(filesAlreadyProcessed, filesToProcess,
                                                    self._validateStagingMonoPath(), self._validateStagingChunksPath(),
                                                    self.ADAPTERNAME)

  def _validateKorpusPath(self):
    korpus_path = self.config['untranscribed_videos_input_adapter']['korpus_path']
    if not os.path.isdir(korpus_path):
      raise IOError("Could not read korpus path" + korpus_path)
    return korpus_path

  def _validateStagingMonoPath(self):
    workdir = self.config['global']['workdir']
    if not os.path.isdir(workdir):
      raise IOError("Could not read workdir path" + workdir)
    workdir = Path(workdir).joinpath("untranscribed_video_staging_mono")
    workdir.mkdir(parents=True, exist_ok=True)
    return str(workdir)

  def _validateStagingChunksPath(self):
    workdir = self.config['global']['workdir']
    if not os.path.isdir(workdir):
      raise IOError("Could not read workdir path" + workdir)
    workdir = Path(workdir).joinpath("untranscribed_video_staging_chunks")
    workdir.mkdir(parents=True, exist_ok=True)
    return str(workdir)

  def _determineVideoFilesToConvertToMono(self):
    originalFiles = set(self._getAllMediaFilesInBasepath(self._validateKorpusPath(), {".mp4"}))
    alreadyStagedFiles = set(self._getAllMediaFilesInBasepath(self._validateStagingMonoPath(), {".wav"}))
    self.logger.debug("Got {} original untranscribed mp4 files to process".format(len(originalFiles)))

    return self.determineFilesToConvertToMonoFromGivenLists(alreadyStagedFiles, originalFiles, self.ADAPTERNAME)


class ChJugendspracheAdapter(UntranscribedMediaSplittingAdapter):
  ADAPTERNAME = "CHJugendspracheAdapter"

  def __init__(self, config):
    super(ChJugendspracheAdapter, self).__init__(config=config)
    self.config = config

  def toMetamodel(self):
    self.logger.debug("CH-Jugendsprache Korpus")
    # convert audio to mono audio
    filesToProcess, filesAlreadyProcessed = self._determineChJugendspracheFilesToConvertToMono()
    return self._preprocess_workflow_with_splitting(filesAlreadyProcessed, filesToProcess,
                                                    self._validateStagingMonoPath(), self._validateStagingChunksPath(),
                                                    self.ADAPTERNAME)

  def _determineChJugendspracheFilesToConvertToMono(self):
    originalFiles = set(self._getAllMediaFilesInBasepath(self._validateKorpusPath(), {".WAV", ".wav"}))
    alreadyStagedFiles = set(self._getAllMediaFilesInBasepath(self._validateStagingMonoPath(), {".wav"}))
    self.logger.debug("Got {} original jugendsprache files to process".format(len(originalFiles)))

    return self.determineFilesToConvertToMonoFromGivenLists(alreadyStagedFiles, originalFiles, self.ADAPTERNAME)

  def _validateStagingMonoPath(self):
    workdir = self.config['global']['workdir']
    if not os.path.isdir(workdir):
      raise IOError("Could not read workdir path" + workdir)
    workdir = Path(workdir).joinpath("ch_jugensprache_staging_mono")
    workdir.mkdir(parents=True, exist_ok=True)
    return str(workdir)

  def _validateStagingChunksPath(self):
    workdir = self.config['global']['workdir']
    if not os.path.isdir(workdir):
      raise IOError("Could not read workdir path" + workdir)
    workdir = Path(workdir).joinpath("ch_jugensprache_staging_chunks")
    workdir.mkdir(parents=True, exist_ok=True)
    return str(workdir)

  def _validateKorpusPath(self):
    korpus_path = self.config['ch_jugendsprache_input_adapter']['korpus_path']
    if not os.path.isdir(korpus_path):
      raise IOError("Could not read korpus path" + korpus_path)
    return korpus_path


class ArchimobAdapter(UntranscribedMediaSplittingAdapter):
  """
  ArchimobAdapter currently only converts audio to mono. Metadata-Conversion will be implemented in a later release
  """
  ADAPTERNAME = "Archimob"

  def __init__(self, config):
    super(ArchimobAdapter, self).__init__(config=config)
    self.config = config

  def _validateKorpusPath(self):
    korpus_path = self.config['archimob_input_adapter']['korpus_path']
    if not os.path.isdir(korpus_path):
      raise IOError("Could not read korpus path" + korpus_path)
    return korpus_path

  def _transcription_pause_tag_symbol(self):
    symbol = self.config['archimob_input_adapter']['transcription_pause_tag_symbol']
    if not symbol:
      self.logger.warn("No symbol for transcription pause tag configured, falling back to default, which is '@'-Symbol")
      symbol = '@'
    return symbol

  def _transcription_vocal_tag_symbol(self):
    symbol = self.config['archimob_input_adapter']['transcription_vocal_tag_symbol']
    if not symbol:
      self.logger.warn("No symbol for transcription pause tag configured, falling back to default, which is '#'-Symbol")
      symbol = '#'
    return symbol

  def _validateWorkdir(self):
    workdir = self.config['global']['workdir']
    if not os.path.isdir(workdir):
      raise IOError("Could not read workdir path" + workdir)
    workdir = Path(workdir).joinpath("archimob_staging")
    workdir.mkdir(parents=True, exist_ok=True)
    return str(workdir)

  def _determineArchimobFilesToProcess(self):
    originalFiles = set(self._getAllMediaFilesInBasepath(self._validateKorpusPath(), {".wav"}))
    originalFiles = self._fixOriginalDatasetFlawsIfNecessary(originalFiles)
    alreadyStagedFiles = set(self._getAllMediaFilesInBasepath(self._validateWorkdir(), {".wav"}))
    self.logger.debug("Got {} original archimob files to process".format(len(originalFiles)))

    return self.determineFilesToConvertToMonoFromGivenLists(alreadyStagedFiles, originalFiles, self.ADAPTERNAME)

  def toMetamodel(self):
    self.logger.debug("Archimob V2 Korpus")
    # convert chunks to mono audio
    filesToProcess, filesAlreadyProcessed = self._determineArchimobFilesToProcess()
    filesSuccessfullyProcessed = self.convertMediaFilesToMonoAudio(filesToProcess, self._validateWorkdir(),
                                                                   self.ADAPTERNAME)
    filesForMediaBundle = []
    filesForMediaBundle = filesForMediaBundle + filesSuccessfullyProcessed + filesAlreadyProcessed
    # add chunks to media session
    mediaAnnotationbundles = self.createMediaAnnotationBundles(filesForMediaBundle)
    mediaSession = self.createMediaSession(mediaAnnotationbundles)
    return mediaSession

  def createMediaSession(self, bundles):
    speakers = set([speaker.writtenResource.actorRef for speaker in bundles])
    session = MediaSession(self.ADAPTERNAME, speakers, bundles)
    return session

  def createMediaAnnotationBundles(self, filesForMediaBundle):
    allXmlOriginalTranscriptionFiles = self._archimobOriginalTranscriptionFiles(self._validateKorpusPath())
    transcriptionsPerSpeaker = self._extract(allXmlOriginalTranscriptionFiles)
    mediaFilesAndTranscription = self._onlyTranscriptionsWithMediaFilesAndViceVersa(transcriptionsPerSpeaker,
                                                                                    filesForMediaBundle)
    mediaAnnotationBundles = self._createActualMediaAnnotationBundles(mediaFilesAndTranscription)
    return mediaAnnotationBundles

  def _fixOriginalDatasetFlawsIfNecessary(self, originalFiles):
    # As of Archimobe release V2 there are some minor flaws in the data, which are treated sequentially
    if (self._fixForDuplicateWavs1063Necessary(originalFiles)):
      originalFiles = self._fixForDuplicateWavs1063(originalFiles)

    if (self._fixForWrongFilenames1082Necessary(originalFiles)):
      originalFiles = self._fixForWrongFilenames1082(originalFiles)

    return originalFiles

  def _fixForDuplicateWavs1063Necessary(self, originalFiles):
    # This flaw is simply, that within 1063 there exists another folder 1063 containing all files again
    existingPathsForDoubled1063 = list(
        filter(lambda file: os.path.sep + "1063" + os.path.sep + "1063" + os.path.sep in file, originalFiles))
    fixNecessary = len(existingPathsForDoubled1063) > 0
    self.logger.info("Found {} files of speaker 1063 which are duplicates. They will be ignored".format(
        len(existingPathsForDoubled1063)))
    return fixNecessary

  def _fixForDuplicateWavs1063(self, originalFiles):
    # fix is simply by removing the files in question from list
    pathsWithout1063duplicates = list(
        filter(lambda file: not (os.path.sep + "1063" + os.path.sep + "1063" + os.path.sep in file), originalFiles))
    originalFiles = pathsWithout1063duplicates
    return originalFiles

  def _fixForWrongFilenames1082Necessary(self, originalFiles):
    regexForFindingWrongNames = "(^\d{4}_\d)(d\d{4}_.*\.wav)"  # like 1082_2d1082_2_TLI_3.wav
    onlyFilenames = [os.path.basename(filename) for filename in originalFiles]
    for filename in onlyFilenames:
      m = re.search(regexForFindingWrongNames, filename)
      if (not (m is None)):
        return True
    return False

  def _fixForWrongFilenames1082(self, originalFiles):
    fixedFiles = originalFiles.copy()
    regexForFindingWrongFullpaths = "(.*\\" + os.path.sep + ")(\d{4}_\d)(d\d{4}_.*\.wav)"  # like /home/somebody/files/1082/1082_2d1082_2_TLI_3.wav
    for filename in originalFiles:
      m = re.search(regexForFindingWrongFullpaths, filename)
      if (not (m is None)):
        newFilename = m.group(1) + m.group(3)
        self.logger.debug(
            "Fix 1082: Renaming file {} from {} to {}".format(m.group(2) + m.group(3), filename, newFilename))
        try:
          shutil.move(filename, newFilename)
          fixedFiles.add(newFilename)
        except Exception as inst:
          self.logger.warn(
              "Could not move file {} to {}, skipping and just removing from usable filenames".format(filename,
                                                                                                      newFilename),
              exc_info=inst)
        fixedFiles.remove(filename)
    return fixedFiles

  def _archimobOriginalTranscriptionFiles(self, path):
    xmlOriginalFiles = list(Path(path).glob("**/*.xml"))
    self.logger.debug("Found {} original xml files for archimob".format(len(xmlOriginalFiles)))
    return xmlOriginalFiles

  def _extract(self, allXmlOriginalTranscriptionFiles):
    transcriptionsPerSpeaker = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
      futures = []
      for filenumber, file in enumerate(allXmlOriginalTranscriptionFiles):
        futures.append(executor.submit(self._extractSingleXmlFileThread, file))
    for future in as_completed(futures):
      if (future.result()[0] == False):
        self.logger.warning("Couldnt extract metadata for file {}, removing from list".format(future.result()[1]))
      else:
        transcriptionsPerSpeaker.append(
            (future.result()[1], future.result()[2]))  # tuple of original file and transcription dataframe
      self.logger.debug("Extracting metadata for speaker finished {}".format(future.result()))
    self.logger.debug("Finished metadata extraction for all {} xml files".format(len(allXmlOriginalTranscriptionFiles)))
    return transcriptionsPerSpeaker

  def _extractSingleXmlFileThread(self, xmlFile):
    namespaceprefix = "{http://www.tei-c.org/ns/1.0}"

    try:
      tree = ET.parse(xmlFile)
      root = tree.getroot()
      de_data = pd.DataFrame(columns=['Filename', 'transcript'])
      transcriptionForSpeaker = pd.DataFrame(columns=de_data.columns)
      tagsToIgnore = set([namespaceprefix + tag for tag in {"gap", "incident", "kinesic", "other"}])

      for utteranceTag in root.iter(namespaceprefix + 'u'):
        media = utteranceTag.attrib['start']
        filename = media.split('#')[1]

        ch_transcript = [""]
        for element in utteranceTag:
          extractedWord = ""
          if (namespaceprefix + "w" == element.tag):
            extractedWord = self._extractWordTag(element)
          if (namespaceprefix + "pause" == element.tag):
            extractedWord = self._extractPauseTag(element)
          if (namespaceprefix + "vocal" == element.tag):
            extractedWord = self._extractVocalTag(namespaceprefix, element)
          if (namespaceprefix + "del" == element.tag):
            extractedWord = self._extractDeletionTag(element)
          if (namespaceprefix + "unclear" == element.tag):
            extractedWord = self._extractUnclearTag(namespaceprefix, element)
          if (element.tag in tagsToIgnore):
            self.logger.debug(
                "Found tag {} which is in ignore list, ignoring the whole utterance {}".format(element.tag, filename))
            break

          if (extractedWord):
            cleanedWord = self._cleanExtractedWord(extractedWord)
            if (cleanedWord):
              ch_transcript.append(cleanedWord)

        try:
          actualTranscript = " ".join(ch_transcript).strip()
          if (not actualTranscript or (self._transcription_pause_tag_symbol() == actualTranscript)):
            self.logger.debug("Skipping empty transcription for filename {}".format(filename))
            continue
          transcriptionForSpeaker = transcriptionForSpeaker.append(
              {'Filename': filename, 'transcript': actualTranscript}, ignore_index=True)
        except Exception as e:
          self.logger.warn("Couldn't append single utterance for filename {}".format(filename), exc_info=e)
          continue

      # writing is just for manual checking
      transcriptionForSpeaker.to_csv(
          os.path.join(self._getFullFilenameWithoutExtension(xmlFile) + "_transcript_CH.csv"),
          header=True, index=False, encoding='utf-8')

      return True, xmlFile, transcriptionForSpeaker

    except Exception as e:
      self.logger.warn("Couldn't extract metadata for xml file {}".format(xmlFile), exc_info=e)
    return False, xmlFile, None

  def _extractWordTag(self, element):
    return element.text

  def _extractPauseTag(self, element):
    return self._transcription_pause_tag_symbol()

  def _extractVocalTag(self, namespaceprefix, element):
    desc = element.find(namespaceprefix + "desc")
    if desc is not None:
      return self._transcription_vocal_tag_symbol() + desc.text
    return ""

  def _extractDeletionTag(self, element):
    truncatedTextWithPotentialSlash = element.text
    if truncatedTextWithPotentialSlash:
      truncatedText = truncatedTextWithPotentialSlash.replace("/", "")
      return truncatedText
    return ""

  def _extractUnclearTag(self, namespaceprefix, element):
    if element is not None:
      wordsWithinUnclearTag = element.findall(namespaceprefix + 'w')
      unclearText = []
      for word in wordsWithinUnclearTag:
        unclearText.append(word.text)
      return " ".join(unclearText)
    return ""

  def _cleanExtractedWord(self, extractedWord):
    # replace all tokens with gravis with their counterpart    
    # remove all chars not in allowed list
    # Note: q,x and y are not allowed, as thos are not existing within transcription of archimob!
    allowed_chars = {
      'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'w', 'z',
      'ä', 'ö', 'ü',
      ' '
    }
    allowed_chars.add(self._transcription_pause_tag_symbol())
    allowed_chars.add(self._transcription_vocal_tag_symbol())
    whitespace_regex = re.compile(r'[ \t]+')

    extractedWord = extractedWord.lower()
    extractedWord = extractedWord.replace('á', 'a')
    extractedWord = extractedWord.replace('à', 'a')
    extractedWord = extractedWord.replace('â', 'a')
    extractedWord = extractedWord.replace('ç', 'c')
    extractedWord = extractedWord.replace('é', 'e')
    extractedWord = extractedWord.replace('è', 'e')
    extractedWord = extractedWord.replace('ê', 'e')
    extractedWord = extractedWord.replace('í', 'i')
    extractedWord = extractedWord.replace('ì', 'i')
    extractedWord = extractedWord.replace('î', 'i')
    extractedWord = extractedWord.replace('ñ', 'n')
    extractedWord = extractedWord.replace('ó', 'o')
    extractedWord = extractedWord.replace('ò', 'o')
    extractedWord = extractedWord.replace('ô', 'o')
    extractedWord = extractedWord.replace('ú', 'u')
    extractedWord = extractedWord.replace('ù', 'u')
    extractedWord = extractedWord.replace('ǜ', 'u')
    extractedWord = extractedWord.replace('û', 'u')
    extractedWord = extractedWord.replace('ș', 's')
    extractedWord = extractedWord.replace('ş', 's')
    extractedWord = extractedWord.replace('ß', 'ss')
    extractedWord = extractedWord.replace('-', ' ')
    # Those should not exist anymore, however, be safe
    extractedWord = extractedWord.replace('–', ' ')
    extractedWord = extractedWord.replace('/', ' ')
    extractedWord = whitespace_regex.sub(' ', extractedWord)
    extractedWord = ''.join([char for char in extractedWord if char in allowed_chars])
    extractedWord = whitespace_regex.sub(' ', extractedWord)
    extractedWord = extractedWord.strip()

    return extractedWord

  def _onlyTranscriptionsWithMediaFilesAndViceVersa(self, transcriptionsPerSpeaker, filesForMediaBundle):
    if not transcriptionsPerSpeaker or not filesForMediaBundle:
      return []

    existingMediaFilesTuples = [(self._getFilenameWithoutExtension(mediafile), mediafile) for mediafile in
                                filesForMediaBundle]
    existingMediaFiles, existingMediaFilesFullpath = zip(*existingMediaFilesTuples)

    # combine all transcriptions
    allTranscriptions = pd.concat([transcription[1] for transcription in transcriptionsPerSpeaker])
    if any("-" in filename for filename in allTranscriptions.Filename) \
        and not any("-" in filename for filename in existingMediaFiles):
      self.logger.debug(
          "Found filenames with dash (-) instead of underscore (_) but only filenames with underscore. Automatically fixing this...")
      allTranscriptions.Filename = allTranscriptions.Filename.str.replace("-", "_")

    # Find all files that exist in both sets
    allMatchingTranscriptions = allTranscriptions[allTranscriptions.Filename.isin(existingMediaFiles)].copy()
    allMatchingTranscriptions["FullpathFilename"] = ""
    for filenumber, existingFile in enumerate(existingMediaFiles):
      allMatchingTranscriptions.loc[allMatchingTranscriptions["Filename"] == existingFile, "FullpathFilename"] = \
        existingMediaFilesFullpath[filenumber]

    return allMatchingTranscriptions[["FullpathFilename", "transcript"]].copy()

  def _createActualMediaAnnotationBundles(self, mediaFilesAndTranscription):

    bundles = []
    for fileAndTranscription in mediaFilesAndTranscription.itertuples(index=False):
      bundle = MediaAnnotationBundle(fileAndTranscription.FullpathFilename)
      speakerId = self._speakerIdFromFullpath(fileAndTranscription.FullpathFilename)
      bundle.setMediaFile(MediaFile(speakerId))
      written_resource = WrittenResource(fileAndTranscription.transcript, speakerId, languageCode="CH",
                                         annotationType=WrittenResource.DIETH_WITHOUT_GRAVIS)
      bundle.setWrittenResource(written_resource)
      bundles.append(bundle)

    self.logger.debug("Created {} mediaAnnotationBundles out of {} transcriptions".format(len(bundles), len(
        mediaFilesAndTranscription)))
    return bundles

  def _speakerIdFromFullpath(self, fullpathFilename):
    return self._getFilenameWithoutExtension(fullpathFilename).split("_")[0]


class CommonVoiceAdapter(Adapter):
  RELATIVE_PATH_TO_AUDIO = "clips"
  LANGUAGECODE_DE = "de_DE"
  ADAPTERNAME = "CommonVoiceDE"
  mediaAnnotationBundles = []
  mediaSessionActors = set()  # using a set so we don't have duplets

  def __init__(self, config):
    super(CommonVoiceAdapter, self).__init__(config=config)
    self.config = config

  def toMetamodel(self):
    self.logger.debug("Created CommonVoice Adapter")
    self.audiofilenames = self._readExistingAudioFiles()
    self.speakermetadata = self._readExistingSpeakerMetadata()
    self._persistMetamodel()
    self._buildMediaSession()
    return self.mediaSession

  def _validateKorpusPath(self):
    korpus_path = self.config['common_voice_input_adapter']['korpus_path']
    if not os.path.isdir(korpus_path):
      raise IOError("Could not read korpus path" + korpus_path)
    return korpus_path

  def _existingAudioFileFullpath(self, filename):
    return os.path.join(self._validateKorpusPath(), self.RELATIVE_PATH_TO_AUDIO, filename)

  def _readExistingAudioFiles(self):
    fullpath = os.path.join(self._validateKorpusPath(), self.RELATIVE_PATH_TO_AUDIO)
    for file in os.listdir(fullpath):
      if file.endswith(".mp3"):
        currentfile = MediaAnnotationBundle(self._existingAudioFileFullpath(file))
        self.mediaAnnotationBundles.append(currentfile)
    self.logger.debug("Found {} audiofiles to process".format(len(self.mediaAnnotationBundles)))
    pass

  def _readExistingSpeakerMetadata(self, ):
    existing_audio_identifier = self._getFilenamesFromMediaAnnotationBundles()
    common_voice_valid_metadata = self._getCommonVoiceValidMetadata(
        existing_audio_identifier, self._validateKorpusPath())

    self._enrichWithTranscription(common_voice_valid_metadata)
    self._extractMediaSessionActors(common_voice_valid_metadata)

  def _enrichWithTranscription(self, common_voice_valid_metadata):
    self.mediaAnnotationBundles_dictionary_withoutExtension = {self._getFilenameWithoutExtension(x.identifier): x for x
                                                               in self.mediaAnnotationBundles}
    self.mediaAnnotationBundles_dictionary_withExtension = {self._getFilenameWithExtension(x.identifier): x for x in
                                                            self.mediaAnnotationBundles}
    common_voice_valid_metadata.apply(self._enrichWithTranscriptionInner, axis=1)
    pass

  def _enrichWithTranscriptionInner(self, row):
    currentMediaAnnotationBundle = self.mediaAnnotationBundles_dictionary_withoutExtension.get(row.path,
                                                                                               self.mediaAnnotationBundles_dictionary_withExtension.get(
                                                                                                   row.path))
    currentMediaAnnotationBundle.setWrittenResource(
        WrittenResource(row.sentence, row.client_id, self.LANGUAGECODE_DE))
    currentMediaAnnotationBundle.setMediaFile(MediaFile(row.client_id))
    self.logger.debug(
        "Found matching media-annotation bundle for identifier {} and path {}".format(row.client_id, row.path))

  def _extractMediaSessionActors(self, common_voice_valid_metadata):
    common_voice_valid_metadata.apply(self._createMediaSessionActorFromRow, axis=1)
    self.logger.debug("Found {} Speakers".format(len(self.mediaSessionActors)))

  pass

  def _createMediaSessionActorFromRow(self, row):
    self.mediaSessionActors.add(MediaSessionActor(row.client_id, Sex.toSexEnum(row.gender), row.age))
    pass

  def _getCommonVoiceValidMetadata(self, existing_audio_identifier,
      korpus_path):
    commonvoice_valid_metadatafilenames = ["dev.tsv", "test.tsv", "train.tsv", "validated.tsv"]
    combined_csv = pd.concat(
        [pd.read_csv(os.path.join(korpus_path, f), sep="\t", header=0) for f in commonvoice_valid_metadatafilenames])
    common_voice_valid_metadata = combined_csv[combined_csv.path.isin(existing_audio_identifier)]

    common_voice_valid_metadata = self._fixChangeInDataFormatCommonVoice(common_voice_valid_metadata, combined_csv)

    return common_voice_valid_metadata

  def _getFilenamesFromMediaAnnotationBundles(self):
    return [os.path.splitext(os.path.basename(base.identifier))[0] for base in
            self.mediaAnnotationBundles]

  def _getFilenamesFromMediaAnnotationBundlesWithExtension(self):
    return [os.path.basename(base.identifier) for base in self.mediaAnnotationBundles]

  def _persistMetamodel(self):
    # TODO actual persisting of working json
    # Actual json output
    # print(json.dumps(self.mediaAnnotationBundles, default=lambda o: o.__dict__, sort_keys=True, indent=4))
    pass

  def _buildMediaSession(self):
    actors = MediaSessionActors(self.mediaSessionActors)
    session = MediaSession(self.ADAPTERNAME, actors, self.mediaAnnotationBundles)
    # TODO Validate
    self.mediaSession = session
    pass

  def _fixChangeInDataFormatCommonVoice(self, common_voice_valid_metadata, combined_csv):
    if (len(common_voice_valid_metadata) == 0):
      self.logger.debug(
          "CommonVoice tsv-files seem to have filename-extension set (new fileformat). Trying matching with extension")
      common_voice_valid_metadata = combined_csv[
        combined_csv.path.isin(self._getFilenamesFromMediaAnnotationBundlesWithExtension())]
    self.logger.debug(
        "CommonVoice Valid metadata length is: {}".format(len(common_voice_valid_metadata)))
    return common_voice_valid_metadata
