import concurrent
import itertools
import os
import random
import shutil
from concurrent.futures import as_completed
from datetime import datetime
from statistics import mean, stdev, median
from time import gmtime, strftime

import librosa
import pandas
import soundfile
from quantulum3 import parser

from audio_korpora_pipeline.baseobjects import FileHandlingObject
from audio_korpora_pipeline.metamodel.mediasession import MediaSession
from audio_korpora_pipeline.utils import winapi_path


class Adapter(FileHandlingObject):
  def __init__(self, config):
    super(Adapter, self).__init__()

  def fromMetamodel(self, mediaSession):
    raise NotImplementedError("Please use a subclass")

  def skipAlreadyProcessedFiles(self):
    skip = self.config['global']['skipAlreadyProcessedFiles']
    if not (skip):
      self.logger.warn("No config setting for skipAlreadyProcessedFiles set. Assuming True")
      return True
    return skip

  def cleanOutputFolder(self):
    if (self.skipAlreadyProcessedFiles()):
      self.logger.info("Cleaning of output folder is ignored, as Parameter skipAlreadyProcessedFiles is set to true")
      return
    self.logger.debug("Cleaning workdirectory {}".format(self._basePath()))
    # making sure all are empty when we start the process:
    shutil.rmtree(self._basePath(), ignore_errors=True)
    os.makedirs(self._basePath(), exist_ok=True)

  def _validateBasePath(self):
    outputPath = self._basePath()
    if not os.path.isdir(outputPath):
      raise IOError("Could not read korpus path" + outputPath)
    return outputPath

  def _determineLanguages(self, mediaSession):
    languages = [(wr.language) for wr in
                 (bundle.writtenResource for bundle in mediaSession.mediaAnnotationBundles if bundle.valid())]

    language_set = set(languages)
    self.logger.debug("Found {} Language(s) for MAILABS".format(len(language_set)))
    return language_set

  def _determineGenders(self, mediaSession):
    actors = mediaSession.mediaSessionActors.mediaSessionActors
    genders = [actor.sex for actor in actors]
    gender_set = set(genders)
    self.logger.debug("Found {} Gender(s) for MAILABS".format(len(gender_set)))
    return gender_set

  def _determineSpeaker(self, mediaSession):
    actors = mediaSession.mediaSessionActors.mediaSessionActors
    speakers = [actor for actor in actors]
    speaker_set = set(speakers)
    self.logger.debug("Found {} Speakers(s) for MediaSession".format(len(speaker_set)))
    return speaker_set

  def _getFilenameWithoutExtensionFromBundle(self, fullpath):
    return os.path.splitext(os.path.basename(fullpath))[0]

  def _getFilenameWithExtension(self, fullpath):
    return os.path.basename(fullpath)

  def _actuallyWritingAudioToFilesystemThread(self, currentFolder, fullpathToFile, samplerate=16000):
    os.makedirs(currentFolder, exist_ok=True)

    try:
      # propably very slow, because loads floating-points...
      y3, sr3 = librosa.load(fullpathToFile, sr=samplerate, mono=True)
      targetAudioFileName = os.path.join(currentFolder,
                                         os.path.splitext(os.path.basename(fullpathToFile))[
                                           0] + ".wav")
      soundfile.write(targetAudioFileName, y3, samplerate=samplerate, subtype='PCM_16')
    except:
      return (False, str(fullpathToFile))
    return (True, str(fullpathToFile))

  def _resampleAndCopyAudioFiles(self, mediaSession, foldernames, sampleRate, functionToDetermineNextFolder):
    self.logger.debug("Starting prepare and move audiofiles")
    for counter, mediaAnnotationBundle in enumerate(mediaSession.mediaAnnotationBundles):
      self.logger.debug("Processing Audio number {} form {}".format(counter, len(mediaSession.mediaAnnotationBundles)))
      currentWrittenResource = mediaAnnotationBundle.writtenResource

      writingAudioToFilesystemList = []
      if currentWrittenResource is not None:
        currentFolder = functionToDetermineNextFolder(currentWrittenResource, foldernames)
        currentFolder = os.path.join(currentFolder, "wavs")
        writingAudioToFilesystemList.append((currentFolder, mediaAnnotationBundle.identifier))

      with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        futures = [executor.submit(self._actuallyWritingAudioToFilesystemThread, entry[0], entry[1], sampleRate) for
                   entry in
                   writingAudioToFilesystemList]
      for future in as_completed(futures):
        if (future.result()[0] == False):
          # FIXME do actually remove audio from metadata
          self.logger.warning("Couldnt process audiofile {}, removing from list".format(future.result()[1]))
        self.logger.debug("Processing Audio is done {}".format(future.result()))
    pass


class LjSpeechAdapter(Adapter):
  def __init__(self, config):
    super(LjSpeechAdapter, self).__init__(config=config)
    self.config = config

  def fromMetamodel(self, mediaSession):
    if not isinstance(mediaSession, MediaSession):
      raise ValueError("MediaSession must not be None and must be of type MediaSession")

    self.logger.debug("LJSpeech Starting actual work at {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    foldernames = self._createFolderStructureAccordingToLjSpeech(mediaSession)

    self.logger.debug("Actual foldernames are {}".format(foldernames))

    self._createMetadatafiles(mediaSession, foldernames)
    self._resampleAndCopyAudioFilesLjSpeech(mediaSession, foldernames)
    self._validateProcess(mediaSession)

    pass

  def _combine_multiple_speakers_into_one_dataset(self):
    return self.config.getboolean('ljspeech_output_adapter', 'combine_multiple_speakers_into_one_dataset')

  def _basePath(self):
    return self.config['ljspeech_output_adapter']['output_path']

  def _createFolderStructureAccordingToLjSpeech(self, mediaSession):
    """

    :return: list of foldernames
    """
    if (self._combine_multiple_speakers_into_one_dataset() == True):
      self.logger.debug("Multiple speaker should be merged into one dataset as config is set to :{}".format(
          self._combine_multiple_speakers_into_one_dataset()))
      foldernames = [self._basePath()]
    else:
      self.logger.debug("Multiple speaker will be in seperate output folders, as config is set to :{}".format(
          self._combine_multiple_speakers_into_one_dataset()))
      speakers = self._determineSpeaker(mediaSession)
      foldernames = [os.path.join(self._basePath(), currentSpeaker.id) for currentSpeaker in speakers]
    self.logger.debug("Foldernames for LJSpeech are {}".format(foldernames))

    foldernames = [winapi_path(folder) for folder in foldernames]

    for foldername in foldernames:
      foldernameWithWavs = os.path.join(foldername, "wavs")
      os.makedirs(foldernameWithWavs, exist_ok=True)
    return foldernames

  def _createMetadatafiles(self, mediaSession, foldernames):
    self.logger.debug("Starting metadatafile-creation ljspeech")
    for mediaAnnotationBundle in mediaSession.mediaAnnotationBundles:
      currentWrittenResource = mediaAnnotationBundle.writtenResource
      if currentWrittenResource is not None:
        if (self._combine_multiple_speakers_into_one_dataset() == True):
          currentFolder = next(iter(foldernames))
        else:
          currentFolder = self._determineNextFoldernameLJSpeech(currentWrittenResource, foldernames)
        # creating file
        filepath = os.path.join(currentFolder, "metadata.csv")
        # appending to file if present
        open(filepath, 'a', encoding="UTF-8", newline="\n").close()
        normalizedText = self._normalizeText(currentWrittenResource)
        with open(filepath, 'a', encoding="UTF-8", newline="\n") as fd:
          fd.write(self._getFilenameWithoutExtensionFromBundle(
              mediaAnnotationBundle.identifier) + "|" + currentWrittenResource.name + "|" + normalizedText + "\n")
    pass

  def _normalizeText(self, writtenResource):
    """
    Normalize abbreviations, numbers and other quantities to written full-words
    FIXME quantulum does not support german right now, should use: writtenResource.language.ISO639
    :param writtenResource: written ressource should not be null
    :return: normalized text
    """
    return parser.inline_parse_and_expand(writtenResource.name, lang='en_US')

  def _resampleAndCopyAudioFilesLjSpeech(self, mediaSession, foldernames):
    self.logger.debug("Starting prepare and move audiofiles LjSpeech")
    self._resampleAndCopyAudioFiles(mediaSession, foldernames, 22500, self._determineNextFoldernameLJSpeech)
    pass

  def _determineNextFoldernameLJSpeech(self, currentWrittenResource, foldernames):
    if (self._combine_multiple_speakers_into_one_dataset() == True):
      return foldernames[0]
    return next(folder for folder in foldernames if currentWrittenResource.actorRef in folder)

  def _validateProcess(self, mediaSession):
    """
    FIXME should be implemented
    :param mediaSession:
    :return:
    """
    self.logger.debug("Validate LJSpeech")
    pass


class MailabsAdapter(Adapter):
  def fromMetamodel(self, mediaSession):
    if not isinstance(mediaSession, MediaSession):
      raise ValueError("MediaSession must not be None and must be of type MediaSession")

    self.logger.debug("Starting actual work at {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    foldernames = self._createFolderStructureAccordingToMailabs(mediaSession)
    self._createMetadatafiles(mediaSession, foldernames)
    self._resampleAndCopyAudioFilesMailabs(mediaSession, foldernames)
    self._validateProcess(mediaSession)
    pass

  def _basePath(self):
    return self.config['mailabs_output_adapter']['output_path']

  def _outputPath(self):
    return os.path.join(self._basePath(), "output_MAILABS")

  def __init__(self, config):
    super(MailabsAdapter, self).__init__(config=config)
    self.config = config

  def _createFolderStructureAccordingToMailabs(self, mediaSession):
    language_set = self._determineLanguages(mediaSession)
    gender_set = self._determineGenders(mediaSession)
    speaker_set = self._determineSpeaker(mediaSession)
    bookname_mailabs = self._determineBookName(mediaSession)

    self.logger.debug("Starting prepare folderstructure mailabs")
    foldernames = self._generateFoldernames(language_set, gender_set, speaker_set, bookname_mailabs)
    self.logger.debug("Created the following folders:{}".format(foldernames))
    return foldernames

  def _determineBookName(self, mediaSession):
    bookname = mediaSession.name
    self.logger.debug("Bookname is {}".format(bookname))
    return bookname

  def _createMetadatafiles(self, mediaSession, foldernames):
    self.logger.debug("Starting metadatafile-creation mailabs")
    for mediaAnnotationBundle in mediaSession.mediaAnnotationBundles:
      currentWrittenResource = mediaAnnotationBundle.writtenResource
      if currentWrittenResource is not None:
        currentFolder = next(folder for folder in foldernames if currentWrittenResource.actorRef in folder)
        # creating file
        filepath = os.path.join(currentFolder, "metadata.csv")
        # appending to file if present
        open(filepath, 'a', encoding="UTF-8", newline="\n").close()
        with open(filepath, 'a', encoding="UTF-8", newline="\n") as fd:
          fd.write(self._getFilenameWithoutExtensionFromBundle(
              mediaAnnotationBundle.identifier) + "|" + currentWrittenResource.name + "\n")
        self.logger.debug("Created Metadata for {}".format(currentFolder))
    pass

  def _resampleAndCopyAudioFilesMailabs(self, mediaSession, foldernames):
    self.logger.debug("Starting prepare and move audiofiles mailabs")
    self._resampleAndCopyAudioFiles(mediaSession, foldernames, 16000, self._mailabsFunctionToDetermineNextFolder)
    pass

  def _mailabsFunctionToDetermineNextFolder(self, currentWrittenResource, foldernames):
    currentFolder = next(folder for folder in foldernames if currentWrittenResource.actorRef in folder)
    return currentFolder

  def _validateProcess(self, mediaSession):
    self.logger.debug("Validate mailabs")
    pass

  def _generateFoldernames(self, language_set, gender_set, speaker_set, bookname_mailabs):
    possibleCombinationsOfLanguageAndGender = list(itertools.product(language_set, gender_set))
    combinationPath = [os.path.join(self._basePath(), combination[0].ISO639, "by_book", combination[1].name)
                       for combination in
                       possibleCombinationsOfLanguageAndGender]

    # Loop through speakers and create final list of paths
    finalPaths = []
    for speaker in speaker_set:
      for possiblePath in combinationPath:
        if (speaker.sex.name == os.path.basename(possiblePath)):
          actualFolder = os.path.join(possiblePath, speaker.id, bookname_mailabs)
          # FIXME Windows hack problems on unix?
          # see https://stackoverflow.com/questions/36219317/pathname-too-long-to-open/36219497
          actualFolder = winapi_path(actualFolder)
          finalPaths.append(actualFolder)
          # create folders
          os.makedirs(actualFolder, exist_ok=True)

    self.logger.debug("Found and created {} Outputpaths for MAILABS".format(len(finalPaths)))
    return finalPaths


class FairseqWav2VecAdapter(Adapter):
  def __init__(self, config):
    super(FairseqWav2VecAdapter, self).__init__(config=config)
    self.config = config
    self.rand = random.Random(42)

  def fromMetamodel(self, mediaSession):
    if not isinstance(mediaSession, MediaSession):
      raise ValueError("MediaSession be of type MediaSession")

    self.logger.debug("FairseqWav2Vec Starting actual work at {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    foldername = self._createFolderStructureAccordingToFairseqWav2Vec()

    self.logger.debug("Actual foldername is {}".format(foldername))

    successfulFiles, unsuccessfulFiles = self._resampleAndCopyAudioFilesFairseqWav2Vec(mediaSession)
    self._createMetadatafiles(mediaSession, foldername, unsuccessfulFiles)
    self._validateProcess(mediaSession)

    pass

  def _basePath(self):
    return self.config['fairseq_wav2vec_output_adapter']['output_path']

  def _valid_percent(self):
    return float(self.config['fairseq_wav2vec_output_adapter']['valid_percent'])

  def _createFolderStructureAccordingToFairseqWav2Vec(self):
    """

    :return: there is only one output path, as we dont keep track of source on folder level
    """
    foldername = self._basePath()
    foldername = winapi_path(foldername)
    self.logger.debug("Foldername for FairseqWav2Vec is {}".format(foldername))
    os.makedirs(self._wav_file_path(), exist_ok=True)
    return foldername

  def _createMetadatafiles(self, mediaSession, foldername, unsuccessfulFiles=None):
    if unsuccessfulFiles is None:
      unsuccessfulFiles = {}
    self.logger.debug("Starting metadatafile-creation Fairseq Wav2Vec")

    # creating targetfiles
    filepathTrain = os.path.join(foldername, "train.tsv")
    filepathValid = os.path.join(foldername, "valid.tsv")
    self._createHeaderOfMetadatfileIfNecessary(filepathTrain)
    self._createHeaderOfMetadatfileIfNecessary(filepathValid)

    with open(filepathTrain, 'a', encoding="UTF-8", newline="\n") as train_f, open(filepathValid, 'a', encoding="UTF-8",
                                                                                   newline="\n") as valid_f:
      for mediaAnnotationBundle in mediaSession.mediaAnnotationBundles:
        try:
          if (mediaAnnotationBundle.identifier in unsuccessfulFiles):
            self.logger.debug("Skipping file {} for metadata as it could not successfully be copied before".format(
                mediaAnnotationBundle.identifier))
            continue
          currentFilename = self._getFilenameWithExtension(mediaAnnotationBundle.identifier)
          frames = soundfile.info(mediaAnnotationBundle.identifier).frames
          dest = train_f if self.rand.random() > self._valid_percent() else valid_f
          print('{}\t{}'.format(currentFilename, frames), file=dest)
          self.logger.debug("Wrote filename {} to train or valid metadatafile".format(currentFilename))
        except Exception as excep:
          self.logger.warn(
              "Couldnt get metainformation for file {}. Skipping. This file will not be part of the training set".format(
                  currentFilename), exc_info=excep)
          continue
      self.logger.info(
          "Wrote {} filenames to train and valid metadata files".format(len(mediaSession.mediaAnnotationBundles)))
      self.logger.info(
          "Skipped {} filenames due to previous errors".format(len(unsuccessfulFiles)))
    pass

  def _resampleAndCopyAudioFilesFairseqWav2Vec(self, mediaSession):
    self.logger.debug("Starting prepare and move audiofiles FairseqWav2Vec")
    filesToProcess = [mediaAnnotationBundle.identifier for mediaAnnotationBundle in mediaSession.mediaAnnotationBundles]
    if (self.skipAlreadyProcessedFiles()):
      allExistingWavs = self._getAllMediaFilesInBasepath(self._wav_file_path(), {".wav"})
      filesToProcess = self._determineFilesToResampleAndCopy(filesToProcess, allExistingWavs)

    successfulFilenames = []
    unsuccessfulFilenames = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
      futures = []
      for counter, fileToProcess in enumerate(filesToProcess):
        # we don't use _resampleAndCopyAudioFiles, instead we use more low-level function direct
        futures.append(
            executor.submit(self._actuallyWritingAudioToFilesystemThread, self._wav_file_path(), fileToProcess))
    for future in as_completed(futures):
      if (future.result()[0] == False):
        unsuccessfulFilenames.append(future.result()[1])
        self.logger.warning("Couldn't copy and resample file {}. This file will be skipped".format(future.result()[1]))
      else:
        successfulFilenames.append(future.result()[1])
        self.logger.debug("Copied and resampled file {}.".format(future.result()[1]))
    return successfulFilenames, unsuccessfulFilenames

  def _validateProcess(self, mediaSession):
    """
    :param mediaSession:
    :return:
    """
    self.logger.debug("Validate FairseqWav2Vec")
    self._validate_all_files_named_within_metadata_files_exist()
    self._writeSummary()
    # make sure only files within metadatafiles are mentioned, that exist within wav-folders and vice-versa
    # make sure no duration is less than 1 second (arbitrary size, just longer than zero, e.g. not corrupt)
    pass

  def _createHeaderOfMetadatfileIfNecessary(self, filepath):
    if not (os.path.isfile(filepath)):
      with open(filepath, 'a', encoding="UTF-8", newline="\n") as fd:
        fd.write(self._wav_file_path() + "\n")
        self.logger.debug("Wrote basepath location for wav-files {} as header".format(self._wav_file_path()))
    pass

  def _wav_file_path(self):
    return os.path.join(self._basePath(), "wavs")

  def _determineFilesToResampleAndCopy(self, filesPotentiallyToProcess=[], allExistingWavs=[]):
    allExistingWavs = set(allExistingWavs)
    allExistingWavsWithoutPath = set(map(lambda filename: self._getFilenameWithExtension(filename), allExistingWavs))
    allPotentialWavsWithoutPath = set(
        map(lambda filename: self._getFilenameWithExtension(filename), filesPotentiallyToProcess))

    filenamesOnlyToResample = allPotentialWavsWithoutPath.difference(allExistingWavsWithoutPath)
    fullpathsToResample = list(
        filter(lambda filename: self._getFilenameWithExtension(filename) in filenamesOnlyToResample,
               filesPotentiallyToProcess))
    self.logger.debug(
        "From initially {} potential files to resample {} remain to process as others are already existing and parameter skipAlreadyProcessedFiles is set to True".format(
            len(filesPotentiallyToProcess), len(fullpathsToResample)))
    return fullpathsToResample

  def _validate_all_files_named_within_metadata_files_exist(self):
    minimumFrameLengthForValidAudio = 16000  # 1sec. given that sample-rate is 16k
    allExistingWavs = set(map(lambda filename: self._getFilenameWithExtension(filename),
                              self._getAllMediaFilesInBasepath(self._wav_file_path(), {".wav"})))
    self._validate_tsv_file(allExistingWavs, "train.tsv", minimumFrameLengthForValidAudio)
    self._validate_tsv_file(allExistingWavs, "valid.tsv", minimumFrameLengthForValidAudio)
    pass

  def _validate_tsv_file(self, allExistingWavs, tsvFilename, minimumFrameLengthForValidAudio):
    metadatafile = os.path.join(self._basePath(), tsvFilename)
    with open(metadatafile) as f:
      firstRowOfMetadata = f.readline()
    allFilesMentionedInMetadata = pandas.read_csv(metadatafile, sep="\\t", skiprows=1,
                                                  encoding="UTF-8", header=None)
    allFilesMentionedInMetadata.columns = ["filename", "frames"]
    filesNotBeingCopied = set(allFilesMentionedInMetadata.filename).difference(allExistingWavs)
    filesBeingToShortInFrames = set(
        allFilesMentionedInMetadata[allFilesMentionedInMetadata.frames < minimumFrameLengthForValidAudio].filename)
    allFilesNotOk = filesNotBeingCopied.union(filesBeingToShortInFrames)
    if (len(allFilesNotOk) > 0):
      self.logger.warn(
          "While validating file {} got {} files not being ok (out of {} files), which are therefore removed.\nA backup of the original file is created with suffix unvalidated_backup".format(
              tsvFilename,
              len(allFilesNotOk), len(allFilesMentionedInMetadata)))
      shutil.copyfile(os.path.join(self._basePath(), tsvFilename),
                      os.path.join(self._basePath(), tsvFilename + ".unvalidated_backup"))
      for fileNotOk in allFilesNotOk:
        if (fileNotOk in filesNotBeingCopied):
          self.logger.debug("File {} is not correctly copied, ignoring".format(fileNotOk))
        if (fileNotOk in filesBeingToShortInFrames):
          self.logger.debug("File {} is to short, ignoring".format(fileNotOk))
      allTrainFilesCleaned = allFilesMentionedInMetadata[~allFilesMentionedInMetadata.filename.isin(allFilesNotOk)]
      os.remove(os.path.join(self._basePath(), tsvFilename))
      allTrainFilesCleaned.to_csv(metadatafile, sep="\t", encoding="UTF-8", header=None, index=None,
                                  line_terminator="\n")
      with open(metadatafile, 'r') as original:
        data = original.read()
      with open(metadatafile, 'w', newline="\n") as modified:
        modified.write(firstRowOfMetadata + data)
    else:
      self.logger.info("Validated {} FairseqWav2Vec Metadata successfully".format(tsvFilename))

  def _writeSummary(self):
    filename = os.path.join(self._basePath(), "summary.log")
    with open(filename, 'w', newline="\n") as summaryFile:
      summaryFile.write("Corpus processed on {}\n".format(datetime.now()))
      self._writeStatistics(summaryFile, "train.tsv")
      self._writeStatistics(summaryFile, "valid.tsv")
    pass

  def _statisticsOfMetadataFile(self, filename):
    metadatafile = os.path.join(self._basePath(), filename)
    framerate = 16000
    files = pandas.read_csv(metadatafile, sep="\\t", skiprows=1, encoding="UTF-8", header=None)
    files.columns = ["filename", "frames"]

    totalDurationInSeconds = sum(files.frames / framerate)
    meanDurationInSeconds = mean(files.frames / framerate)
    medianDurationInSeconds = median(files.frames / framerate)
    stdDurationInSeconds = stdev(files.frames / framerate)
    countOfFiles = len(files)
    return countOfFiles, totalDurationInSeconds, meanDurationInSeconds, medianDurationInSeconds, stdDurationInSeconds

  def _writeStatistics(self, filehandle, filename):
    countOfFiles, totalDurationInSeconds, meanDurationInSeconds, medianDurationInSeconds, stdDurationInSeconds = self._statisticsOfMetadataFile(
        filename)
    filehandle.write("\n\n\n--- Statistics for file {} ---\n".format(filename))
    filehandle.write("\nCount of datafiles {}".format(countOfFiles))
    filehandle.write("\nTotal duration in seconds {}".format(totalDurationInSeconds))
    filehandle.write("\nTotal duration in hours {}".format(totalDurationInSeconds / 3600))
    filehandle.write("\nMean duration in seconds {}".format(meanDurationInSeconds))
    filehandle.write("\nMedian duration in seconds {}".format(medianDurationInSeconds))
    filehandle.write("\nStandard deviation of duration in seconds {}".format(stdDurationInSeconds))
    pass

  def cleanOutputFolder(self):
    if (self.skipAlreadyProcessedFiles()):
      self.logger.info(
          "Cleaning of output folder is mostly ignored, as Parameter skipAlreadyProcessedFiles is set to true")
      self.logger.info("Cleaning only train.tsv, valid.tsv and summary file")
      filenamesToDelete = ["train.tsv", "valid.tsv", "summary.log", "train.tsv.unvalidated_backup",
                           "valid.tsv.unvalidated_backup"]
      fullpathToFiles = list(map(lambda filename: os.path.join(self._basePath(), filename), filenamesToDelete))
      for file in fullpathToFiles:
        if (os.path.exists(file)):
          # we do not do any errorhandling as run should break if we start with invalid metadata that cant be deleted
          os.remove(file)
          self.logger.debug("Deleted old existing metadata file {}".format(file))
      return
    else:
      Adapter.cleanOutputFolder(self)


class OpenSeq2SeqAdapter(FairseqWav2VecAdapter):

  def __init__(self, config):
    super(OpenSeq2SeqAdapter, self).__init__(config=config)
    self.config = config

  def fromMetamodel(self, mediaSession):
    if not isinstance(mediaSession, MediaSession):
      raise ValueError("MediaSession be of type MediaSession")

    self.logger.debug("OpenSeq2Seq Starting actual work at {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    foldername = self._createFolderStructureAccordingToOpenSeq2Seq()

    self.logger.debug("Actual foldername is {}".format(foldername))

    successfulFiles, unsuccessfulFiles = self._resampleAndCopyAudioFilesFairseqWav2Vec(mediaSession)
    self._createMetadatafiles(mediaSession, foldername, unsuccessfulFiles)
    self._validateProcess(mediaSession)

    pass

  def _createFolderStructureAccordingToOpenSeq2Seq(self):
    foldername = self._basePath()
    foldername = winapi_path(foldername)
    self.logger.debug("Foldername for OpenSeq2Seq is {}".format(foldername))
    os.makedirs(self._wav_file_path(), exist_ok=True)
    return foldername

  def _basePath(self):
    return self.config['openseq2seq_output_adapter']['output_path']

  def _wav_file_path(self):
    return os.path.join(self._basePath(), "wav_files")

  def _createMetadatafiles(self, mediaSession, foldername, unsuccessfulFiles=None):
    if unsuccessfulFiles is None:
      unsuccessfulFiles = {}
    self.logger.debug("Starting metadatafile-creation Openseq2seq")

    # creating targetfiles
    filepathTrain = os.path.join(foldername, "metadata.csv")
    self._createHeaderOfMetadatfileIfNecessary(filepathTrain)

    with open(filepathTrain, 'a', encoding="UTF-8", newline="\n") as train_f:
      for mediaAnnotationBundle in mediaSession.mediaAnnotationBundles:
        try:
          if (mediaAnnotationBundle.identifier in unsuccessfulFiles):
            self.logger.debug("Skipping file {} for metadata as it could not successfully be copied before".format(
                mediaAnnotationBundle.identifier))
            continue
          fullpathFilename = os.path.join(self._wav_file_path(),
                                          self._getFilenameWithExtension(mediaAnnotationBundle.identifier))
          shortFilename = self._getFilenameWithExtension(fullpathFilename)
          dest = train_f
          filesize = os.path.getsize(fullpathFilename)
          print('{},{},{}'.format(fullpathFilename, filesize, mediaAnnotationBundle.writtenResource.name), file=dest)
          self.logger.debug("Wrote transcription for {} to metadatafile".format(shortFilename))
        except Exception as excep:
          self.logger.warn(
              "Couldnt get metainformation for file {}. Skipping. This file will not be part of the training set".format(
                  fullpathFilename), exc_info=excep)
          continue
      self.logger.info(
          "Wrote {} filenames to metadata file".format(len(mediaSession.mediaAnnotationBundles)))
      self.logger.info(
          "Skipped {} filenames due to previous errors".format(len(unsuccessfulFiles)))
    pass

  def _createHeaderOfMetadatfileIfNecessary(self, filepath):
    if not (os.path.isfile(filepath)):
      with open(filepath, 'a', encoding="UTF-8", newline="\n") as fd:
        header = "wav_filename,wav_filesize,transcript\n"
        fd.write(header)
        self.logger.debug("Wrote {} as openseq2seq header".format(header))
    pass

  def _validateProcess(self, mediaSession):
    self.logger.debug("Validate OpenSeq2Seq")
    # FIXME: Validating
    pass
