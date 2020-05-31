import concurrent
import os
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

  def _createMediaSession(self, bundles):
    session = MediaSession(self.ADAPTERNAME, self.mediaSessionActors, bundles)
    return session

  def _createMediaAnnotationBundles(self, audiochunks):
    annotationBundles = []
    for index, filepath in enumerate(audiochunks):
      bundle = MediaAnnotationBundleWithoutTranscription(identifier=filepath)  # we do not have any written ressources
      bundle.setMediaFile(filepath)
      annotationBundles.append(bundle)
    return annotationBundles

  def _splitAudioToChunks(self, filesToChunk, outputPath):
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

  def _determineWavFilesToChunk(self, baseFilesToChunk, stagingChunkPath):
    allStageIndicatorFilesFullpath = set(
        self._getAllMediaFilesInBasepath(stagingChunkPath, {".stagingComplete"}))
    allExistingChunkedFilesFullpath = set(
        self._getAllMediaFilesInBasepath(stagingChunkPath, {".wav"}))
    allStageIndicatorFiles = [self._getFilenameWithoutExtension(file) for file in allStageIndicatorFilesFullpath]
    allBaseFilesWithoutExtension = set([self._getFilenameWithoutExtension(file) for file in baseFilesToChunk])
    stagingCompleteCorrect = allBaseFilesWithoutExtension.intersection(allStageIndicatorFiles)
    stagingIncompleteCorrect = allBaseFilesWithoutExtension.difference(allStageIndicatorFiles)

    stagingComplete = []
    for fullpath in allExistingChunkedFilesFullpath:
      for filename in stagingCompleteCorrect:
        if filename in fullpath:
          stagingComplete.append(fullpath)

    stagingIncomplete = []
    for fullpath in baseFilesToChunk:
      for filename in stagingIncompleteCorrect:
        if filename in fullpath:
          stagingIncomplete.append(fullpath)

    self.logger.debug("Got {} files not yet chunked".format(len(stagingIncomplete)))
    self.logger.debug("Got {} files chunked".format(len(stagingComplete)))
    return stagingIncomplete, stagingComplete

  def _convertMediaFilesToMonoAudio(self, filesToProcess, outputpath, adapterName):
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

  def _determineFilesToConvertToMonoFromGivenLists(self, alreadyStagedFiles, originalFiles, adaptername):
    notYetProcessed = set([self._getFilenameWithExtension(file) for file in originalFiles]).difference(
        set([self._getFilenameWithExtension(file) for file in alreadyStagedFiles]))
    alreadyProcessed = set([self._getFilenameWithExtension(file) for file in originalFiles]).intersection(
        set([self._getFilenameWithExtension(file) for file in alreadyStagedFiles]))
    fullpathsToNotYetProcessed = []
    for fullpath in originalFiles:
      for filename in notYetProcessed:
        if filename in fullpath:
          fullpathsToNotYetProcessed.append(fullpath)
    fullpathsProcessed = []
    for fullpath in originalFiles:
      for filename in alreadyProcessed:
        if filename in fullpath:
          fullpathsProcessed.append(fullpath)
    self.logger.debug("Got {} files not yet processed for corpus {}".format(len(notYetProcessed), adaptername))
    self.logger.debug("Got {} files already processed for corpus {}".format(len(alreadyProcessed), self.adaptername))
    return fullpathsToNotYetProcessed, fullpathsProcessed


class UntranscribedVideoAdapter(UntranscribedMediaSplittingAdapter):
  ADAPTERNAME = "UntranscribedVideoAdapter"

  def __init__(self, config):
    super(UntranscribedVideoAdapter, self).__init__(config=config)
    self.config = config

  def _validateKorpusPath(self):
    korpus_path = self.config['untranscribed_videos_input_adapter']['korpus_path']
    if not os.path.isdir(korpus_path):
      raise IOError("Could not read korpus path" + korpus_path)
    return korpus_path

  def toMetamodel(self):
    self.logger.debug("Untranscribed Video Korpus")
    # convert video to mono audio
    filesToProcess, filesAlreadyProcessed = self._determineVideoFilesToConvertToMono()
    filesSuccessfullyProcessed = self._convertMediaFilesToMonoAudio(filesToProcess, self._validateStagingMonoPath(),
                                                                    self.ADAPTERNAME)
    baseFilesToChunk = []
    baseFilesToChunk = baseFilesToChunk + filesSuccessfullyProcessed + filesAlreadyProcessed
    # split mono audio to chunks
    filesToChunk, filesAlreadyChunked = self._determineWavFilesToChunk(baseFilesToChunk,
                                                                       self._validateStagingChunksPath())
    filesSuccessfullyChunked = self._splitAudioToChunks(filesToChunk, self._validateStagingChunksPath())
    # add chunks to media session
    mediaBundleFiles = [] + filesSuccessfullyChunked + filesAlreadyChunked
    mediaAnnotationbundles = self._createMediaAnnotationBundles(mediaBundleFiles)
    mediaSession = self._createMediaSession(mediaAnnotationbundles)
    return mediaSession

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

    return self._determineFilesToConvertToMonoFromGivenLists(alreadyStagedFiles, originalFiles, self.ADAPTERNAME)


class ChJugendspracheAdapter(UntranscribedMediaSplittingAdapter):
  ADAPTERNAME = "CHJugendspracheAdapter"

  def __init__(self, config):
    super(ChJugendspracheAdapter, self).__init__(config=config)
    self.config = config

  def _validateKorpusPath(self):
    korpus_path = self.config['ch_jugendsprache_input_adapter']['korpus_path']
    if not os.path.isdir(korpus_path):
      raise IOError("Could not read korpus path" + korpus_path)
    return korpus_path

  def toMetamodel(self):
    self.logger.debug("CH-Jugendsprache Korpus")
    # convert audio to mono audio
    filesToProcess, filesAlreadyProcessed = self._determineChJugendspracheFilesToConvertToMono()
    filesSuccessfullyProcessed = self._convertMediaFilesToMonoAudio(filesToProcess, self._validateStagingMonoPath(),
                                                                    self.ADAPTERNAME)
    baseFilesToChunk = []
    baseFilesToChunk = baseFilesToChunk + filesSuccessfullyProcessed + filesAlreadyProcessed
    # convert mono audio to chunks
    filesToChunk, filesAlreadyChunked = self._determineWavFilesToChunk(baseFilesToChunk,
                                                                       self._validateStagingChunksPath())
    filesSuccessfullyChunked = self._splitAudioToChunks(filesToChunk, self._validateStagingChunksPath())
    # add chunks to media session
    mediaBundleFiles = [] + filesSuccessfullyChunked + filesAlreadyChunked
    mediaAnnotationbundles = self._createMediaAnnotationBundles(mediaBundleFiles)
    mediaSession = self._createMediaSession(mediaAnnotationbundles)
    return mediaSession

  def _determineChJugendspracheFilesToConvertToMono(self):
    originalFiles = set(self._getAllMediaFilesInBasepath(self._validateKorpusPath(), {".WAV"}))
    alreadyStagedFiles = set(self._getAllMediaFilesInBasepath(self._validateStagingMonoPath(), {".wav"}))
    self.logger.debug("Got {} original jugendsprache files to process".format(len(originalFiles)))

    return self._determineFilesToConvertToMonoFromGivenLists(alreadyStagedFiles, originalFiles, self.ADAPTERNAME)

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

  def _validateWorkdir(self):
    workdir = self.config['global']['workdir']
    if not os.path.isdir(workdir):
      raise IOError("Could not read workdir path" + workdir)
    workdir = Path(workdir).joinpath("archimob_staging")
    workdir.mkdir(parents=True, exist_ok=True)
    return str(workdir)

  def toMetamodel(self):
    self.logger.debug("Archimob V2 Korpus")
    # convert chunks to mono audio
    filesToProcess, filesAlreadyProcessed = self._determineArchimobFilesToProcess()
    filesSuccessfullyProcessed = self._convertMediaFilesToMonoAudio(filesToProcess, self._validateWorkdir(),
                                                                    self.ADAPTERNAME)
    filesForMediaBundle = []
    filesForMediaBundle = filesForMediaBundle + filesSuccessfullyProcessed + filesAlreadyProcessed
    # add chunks to media session
    mediaAnnotationbundles = self._createMediaAnnotationBundles(filesForMediaBundle)
    mediaSession = self._createMediaSession(mediaAnnotationbundles)
    return mediaSession

  def _determineArchimobFilesToProcess(self):
    originalFiles = set(self._getAllMediaFilesInBasepath(self._validateKorpusPath(), {".wav"}))
    alreadyStagedFiles = set(self._getAllMediaFilesInBasepath(self._validateWorkdir(), {".wav"}))
    self.logger.debug("Got {} original archimob files to process".format(len(originalFiles)))

    return self._determineFilesToConvertToMonoFromGivenLists(alreadyStagedFiles, originalFiles, self.ADAPTERNAME)


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
