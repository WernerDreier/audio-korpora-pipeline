from baseobjects import LoggingObject
from metamodel.mediasession import MediaSession


class Adapter(LoggingObject):
  def __init__(self, config):
    super(Adapter, self).__init__()

  def fromMetamodel(self, mediaSession):
    raise NotImplementedError("Please use a subclass")


class MailabsAdapter(Adapter):
  def __init__(self, config):
    super(Adapter, self).__init__()

  def fromMetamodel(self, mediaSession):
    if not isinstance(mediaSession, MediaSession):
      raise ValueError("MediaSession must not be None and must be of type MediaSession")

    self._createFolderStructureAccordingToMailabs(mediaSession)
    self._createMetadatafiles(mediaSession)
    self._prepareAndMoveAudioFiles(mediaSession)
    self._validateProcess(mediaSession)

  def _createFolderStructureAccordingToMailabs(self, mediaSession):
    language_set = self._determineLanguages(mediaSession)
    gender_set = self._determineGenders(mediaSession)
    speaker_set = self._determineSpeakerIds(mediaSession)
    bookname_mailabs = self._determineBookName(mediaSession)
    self.logger.debug("Starting prepare folderstructure mailabs")
    pass

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

  def _determineSpeakerIds(self, mediaSession):
    actors = mediaSession.mediaSessionActors.mediaSessionActors
    speakers = [actor.id for actor in actors]
    speaker_set = set(speakers)
    self.logger.debug("Found {} Speakers(s) for MAILABS".format(len(speaker_set)))
    return speaker_set

  def _determineBookName(self, mediaSession):
    bookname = mediaSession.name
    self.logger.debug("Bookname is {}".format(bookname))
    return bookname

  def _createMetadatafiles(self, mediaSession):
    self.logger.debug("Starting metadatafile-creation mailabs")
    pass

  def _prepareAndMoveAudioFiles(self, mediaSession):
    self.logger.debug("Starting prepare and move audiofiles mailabs")
    pass

  def _validateProcess(self, mediaSession):
    self.logger.debug("Validate mailabs")
    pass
