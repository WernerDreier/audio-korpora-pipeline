from baseobjects import LoggingObject


class MediaSession(LoggingObject):
  def __init__(self, name):
    self.name = name


class MediaAnnotationBundle(LoggingObject):

  def __init__(self, identifier):
    self.identifier = identifier

  def setMediaFile(self, mediaFile):
    self.mediaFile = mediaFile

  def setWrittenResource(self, writtenResource):
    self.writtenResource = writtenResource

  def valid(self):
    return (self.writtenResource is not None) & (self.mediaFile is not None)


class MediaFile(LoggingObject):
  TYPE_AUDIO = "audio"

  def __init__(self):
    # we only support audios
    self.type = self.TYPE_AUDIO

  def setActor(self, actor):
    self.actor = actor


class WrittenResource(LoggingObject):

  def __init__(self, filename):
    self.name = filename

  def setActor(self, actor):
    self.actor = actor

  def setLanguage(self, languageCode):
    self.language.ISO639 = languageCode
    self.language.languageName = languageCode
