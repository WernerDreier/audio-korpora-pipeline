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

  def __init__(self, actorRef):
    # we only support audios
    self.type = self.TYPE_AUDIO
    self.actorRef = actorRef

  def setActor(self, actor):
    self.actorRef = actor


class Language:
  def __init__(self, languageCode):
    self.ISO639 = languageCode
    self.languageName = languageCode


class WrittenResource(LoggingObject):
  ORTHOGRAPHIC_TRANSCRIPTION = "Orthographic"

  def __init__(self, transcription, actorRef, languageCode):
    self.language = Language(languageCode)
    self.name = transcription
    self.actorRef = actorRef
    self.annotationType = self.ORTHOGRAPHIC_TRANSCRIPTION

  def setActor(self, actorRef):
    self.actorRef = actorRef

  def setLanguage(self, languageCode):
    self.language = Language(languageCode)
