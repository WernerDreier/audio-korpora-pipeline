import itertools
import os
import shutil
from time import gmtime, strftime

import librosa
from quantulum3 import parser

from baseobjects import LoggingObject
from metamodel.mediasession import MediaSession
from utils import winapi_path


class Adapter(LoggingObject):
  def __init__(self, config):
    super(Adapter, self).__init__()

  def fromMetamodel(self, mediaSession):
    raise NotImplementedError("Please use a subclass")

  def _cleanOutputFolder(self):
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
    self.logger.debug("Found {} Speakers(s) for MAILABS".format(len(speaker_set)))
    return speaker_set

  def _getFilenameWithoutExtensionFromBundle(self, fullpath):
    return os.path.splitext(os.path.basename(fullpath))[0]

  def _actuallyWritingAudioToFilesystem(self, currentFolder, fullpathToFile, samplerate=16000):
    os.makedirs(currentFolder, exist_ok=True)
    # propably very slow, because loads floating-points...
    y3, sr3 = librosa.load(fullpathToFile, sr=samplerate)
    targetAudioFileName = os.path.join(currentFolder,
                                       os.path.splitext(os.path.basename(fullpathToFile))[
                                         0] + ".wav")
    librosa.output.write_wav(targetAudioFileName, y3, sr3)


class LjSpeechAdapter(Adapter):
  def __init__(self, config):
    super(LjSpeechAdapter, self).__init__(config=config)
    self.config = config

  def fromMetamodel(self, mediaSession):
    if not isinstance(mediaSession, MediaSession):
      raise ValueError("MediaSession must not be None and must be of type MediaSession")

    self._cleanOutputFolder()
    self.logger.debug("LJSpeech Starting actual work at {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    foldernames = self._createFolderStructureAccordingToLjSpeech()

    self.logger.debug("Actual foldernames are {}".format(foldernames))

    self._createMetadatafiles(mediaSession, foldernames)
    self._resampleAndCopyAudioFiles(mediaSession, foldernames)
    self._validateProcess(mediaSession)

    pass

  def _combine_multiple_speakers_into_one_dataset(self):
    return self.config['ljspeech_output_adapter']['combine_multiple_speakers_into_one_dataset']

  def _basePath(self):
    return self.config['ljspeech_output_adapter']['output_path']

  def _createFolderStructureAccordingToLjSpeech(self):
    """

    :return: list of foldernames
    """
    if (not self._combine_multiple_speakers_into_one_dataset()):
      raise ValueError("Not yet implemented")
    else:
      foldername = self._basePath()
      foldernameWithWavs = os.path.join(foldername, "wavs")
      os.makedirs(foldernameWithWavs, exist_ok=True)
      return [foldername]

  def _createMetadatafiles(self, mediaSession, foldernames):
    self.logger.debug("Starting metadatafile-creation ljspeech")
    if (not self._combine_multiple_speakers_into_one_dataset()):
      raise ValueError("Not yet implemented")
    else:
      # Assuming only one foldername returned
      assert len(foldernames) == 1
      for mediaAnnotationBundle in mediaSession.mediaAnnotationBundles:
        currentWrittenResource = mediaAnnotationBundle.writtenResource
        if currentWrittenResource is not None:
          currentFolder = next(iter(foldernames))
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

  def _resampleAndCopyAudioFiles(self, mediaSession, foldernames):
    assert len(foldernames) == 1
    for counter, mediaAnnotationBundle in enumerate(mediaSession.mediaAnnotationBundles):
      self.logger.debug("Processing Audio number {} form {}".format(counter, len(mediaSession.mediaAnnotationBundles)))
      self._actuallyWritingAudioToFilesystem(os.path.join(foldernames[0], "wavs"), mediaAnnotationBundle.identifier,
                                             samplerate=22500)
    pass

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

    self._cleanOutputFolder()

    self.logger.debug("Starting actual work at {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    foldernames = self._createFolderStructureAccordingToMailabs(mediaSession)
    self._createMetadatafiles(mediaSession, foldernames)
    self._resampleAndCopyAudioFiles(mediaSession, foldernames)
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
    pass

  def _resampleAndCopyAudioFiles(self, mediaSession, foldernames):
    self.logger.debug("Starting prepare and move audiofiles mailabs")
    for counter, mediaAnnotationBundle in enumerate(mediaSession.mediaAnnotationBundles):
      self.logger.debug("Processing Audio number {} form {}".format(counter, len(mediaSession.mediaAnnotationBundles)))
      currentWrittenResource = mediaAnnotationBundle.writtenResource
      if currentWrittenResource is not None:
        currentFolder = next(folder for folder in foldernames if currentWrittenResource.actorRef in folder)
        currentFolder = os.path.join(currentFolder, "wavs")
        self._actuallyWritingAudioToFilesystem(currentFolder, mediaAnnotationBundle.identifier, 16000)
    pass

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
