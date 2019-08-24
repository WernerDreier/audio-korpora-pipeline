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
    self.logger.debug("Starting prepare folderstructure mailabs")
    pass

  def _createMetadatafiles(self, mediaSession):
    self.logger.debug("Starting metadatafile-creation mailabs")
    pass

  def _prepareAndMoveAudioFiles(self, mediaSession):
    self.logger.debug("Starting prepare and move audiofiles mailabs")
    pass

  def _validateProcess(self, mediaSession):
    self.logger.debug("Validate mailabs")
    pass
