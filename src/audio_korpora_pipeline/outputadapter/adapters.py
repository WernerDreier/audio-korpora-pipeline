import itertools
import os
import shutil

import librosa

from baseobjects import LoggingObject
from metamodel.mediasession import MediaSession
from utils import winapi_path


class Adapter(LoggingObject):
  def __init__(self, config):
    super(Adapter, self).__init__()

  def fromMetamodel(self, mediaSession):
    raise NotImplementedError("Please use a subclass")

  def _validateOutputPath(self):
    outputPath = self.config['mailabs_output_adapter']['output_path']
    if not os.path.isdir(outputPath):
      raise IOError("Could not read korpus path" + outputPath)
    return outputPath


class MailabsAdapter(Adapter):

  def _outputPath(self):
    return os.path.join(self._validateOutputPath(), "output_MAILABS")

  def __init__(self, config):
    super(MailabsAdapter, self).__init__(config=config)
    self.config = config

  def fromMetamodel(self, mediaSession):
    if not isinstance(mediaSession, MediaSession):
      raise ValueError("MediaSession must not be None and must be of type MediaSession")

    foldernames = self._createFolderStructureAccordingToMailabs(mediaSession)
    self._createMetadatafiles(mediaSession, foldernames)
    self._resampleAndCopyAudioFiles(mediaSession, foldernames)
    self._validateProcess(mediaSession)

  def _createFolderStructureAccordingToMailabs(self, mediaSession):
    language_set = self._determineLanguages(mediaSession)
    gender_set = self._determineGenders(mediaSession)
    speaker_set = self._determineSpeaker(mediaSession)
    bookname_mailabs = self._determineBookName(mediaSession)

    self.logger.debug("Starting prepare folderstructure mailabs")
    foldernames = self._generateFoldernames(language_set, gender_set, speaker_set, bookname_mailabs)
    self.logger.debug("Created the following folders:{}".format(foldernames))
    return foldernames

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
        open(filepath, 'a').close()
        with open(filepath, 'a') as fd:
          fd.write(self._getFilenameWithoutExtensionFromBundle(
              mediaAnnotationBundle.identifier) + "|" + currentWrittenResource.name + "\n")
    pass

  def _getFilenameWithoutExtensionFromBundle(self, fullpath):
    return os.path.splitext(os.path.basename(fullpath))[0]

  def _resampleAndCopyAudioFiles(self, mediaSession, foldernames):
    self.logger.debug("Starting prepare and move audiofiles mailabs")
    for counter, mediaAnnotationBundle in enumerate(mediaSession.mediaAnnotationBundles):
      self.logger.debug("Processing Audio number {} form {}".format(counter, len(mediaSession.mediaAnnotationBundles)))
      currentWrittenResource = mediaAnnotationBundle.writtenResource
      if currentWrittenResource is not None:
        currentFolder = next(folder for folder in foldernames if currentWrittenResource.actorRef in folder)
        currentFolder = os.path.join(currentFolder, "wavs")
        os.makedirs(currentFolder, exist_ok=True)
        # propably very slow, because loads floating-points...
        y3, sr3 = librosa.load(mediaAnnotationBundle.identifier, sr=16000)
        targetAudioFileName = os.path.join(currentFolder,
                                           os.path.splitext(os.path.basename(mediaAnnotationBundle.identifier))[
                                             0] + ".wav")
        librosa.output.write_wav(targetAudioFileName, y3, sr3)
    pass

  def _validateProcess(self, mediaSession):
    self.logger.debug("Validate mailabs")
    pass

  def _generateFoldernames(self, language_set, gender_set, speaker_set, bookname_mailabs):
    merged = list(itertools.chain.from_iterable([language_set, gender_set]))
    possibleCombinationsOfLanguageAndGender = list(itertools.combinations(merged, 2))
    combinationPath = [os.path.join(self._outputPath(), combination[0].ISO639, "by_book", combination[1].name)
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

          # making sure all are empty when we start the process:
          shutil.rmtree(actualFolder, ignore_errors=True)
          # create folders
          os.makedirs(actualFolder, exist_ok=True)

    self.logger.debug("Found and created {} Outputpaths for MAILABS".format(len(finalPaths)))
    return finalPaths
