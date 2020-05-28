from enum import Enum

from audio_korpora_pipeline.baseobjects import LoggingObject


class Sex(Enum):
  UNKNOWN = 0
  MALE = 1
  FEMALE = 2

  @staticmethod
  def toSexEnum(genderstring='Unknown'):
    genderstring = str(genderstring)
    if (genderstring == "male"):
      return Sex.MALE
    if (genderstring == "female"):
      return Sex.FEMALE
    return Sex.UNKNOWN


class MediaAnnotationBundle(LoggingObject):

  def __init__(self, identifier):
    self.identifier = identifier
    self.writtenResource = None
    self.mediaFile = None

  def setMediaFile(self, mediaFile):
    self.mediaFile = mediaFile

  def setWrittenResource(self, writtenResource):
    self.writtenResource = writtenResource

  def valid(self):
    return (self.writtenResource is not None) & (self.mediaFile is not None)


class MediaAnnotationBundleWithoutTranscription(MediaAnnotationBundle):

  def __init__(self, identifier):
    MediaAnnotationBundle.__init__(self, identifier=identifier)

  # this is a special type not carrying any transcription and therefore must be empty
  def valid(self):
    return (self.writtenResource is None) & (self.mediaFile is not None)


class MediaFile(LoggingObject):
  TYPE_AUDIO = "audio"

  def __init__(self, actorRef):
    # we only support audios
    self.type = self.TYPE_AUDIO
    self.actorRef = actorRef

  def setActor(self, actor):
    self.actorRef = actor


class Language(LoggingObject):
  def __init__(self, languageCode):
    self.ISO639 = languageCode
    self.languageName = languageCode

  def __eq__(self, other):
    if isinstance(other, Language):
      return self.ISO639 == other.ISO639
    else:
      return False

  def __hash__(self):
    return hash(self.__repr__())


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


class MediaSessionActors(LoggingObject):
  def __init__(self, actors=None):
    if actors is None:
      actors = []
    self.mediaSessionActors = actors


class MediaSessionActor(LoggingObject):
  def __init__(self, id, sex=Sex.UNKNOWN, age=None):
    self.id = id
    self.sex = sex
    if age is not None:
      self.age = age

  def __eq__(self, other):
    if isinstance(other, MediaSessionActor):
      return ((self.id == other.id))
    else:
      return False

  def __hash__(self):
    return hash(self.__repr__())


class MediaSession(LoggingObject):
  def __init__(self, name, mediaSessionActors=None, mediaAnnotationBundles=[]):
    self.mediaSessionActors = mediaSessionActors
    self.mediaAnnotationBundles = mediaAnnotationBundles
    self.name = name

  def __repr__(self):
    return "MediaSession(%s, %s,%s)" % (self.name, self.mediaSessionActors, self.mediaAnnotationBundles)
