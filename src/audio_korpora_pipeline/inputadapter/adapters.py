import os

from baseobjects import LoggingObject
from metamodel.mediasession import MediaAnnotationBundle


class Adapter(LoggingObject):
  def __init__(self, config):
    super(Adapter, self).__init__()

  def toMetamodel(self):
    raise NotImplementedError("Please use a subclass")


class ArchimobAdapter(Adapter):
  def __init__(self, config):
    super(ArchimobAdapter, self).__init__(config=config)

  def toMetamodel(self):
    self.logger.debug("hello archomob input adapter")


class CommonVoiceAdapter(Adapter):
  RELATIVE_PATH_TO_AUDIO = "clips"
  mediaAnnotationBundles = []

  def __init__(self, config):
    super(CommonVoiceAdapter, self).__init__(config=config)
    self.config = config

  def toMetamodel(self):
    self.logger.debug("hello CommonVoice Adapter")
    # print(self.config)
    self.logger.debug(self.config['common_voice_input_adapter']['korpus_path'])
    korpus_path = self.config['common_voice_input_adapter']['korpus_path']
    if not os.path.isdir(korpus_path):
      raise IOError("Could not read korpus path" + korpus_path)

    self.audiofilenames = self._readExistingAudioFiles(korpus_path)
    self.speakermetadata = self._readExistingSpeakerMetadta(korpus_path)

    pass

  def _readExistingAudioFiles(self, korpus_path):
    fullpath = os.path.join(korpus_path, self.RELATIVE_PATH_TO_AUDIO)
    for file in os.listdir(fullpath):
      if file.endswith(".mp3"):
        currentfile = MediaAnnotationBundle(file)
        self.mediaAnnotationBundles.append(currentfile)
    self.logger.debug(
        "Found {} audiofiles to process".format(
          len(self.mediaAnnotationBundles)))
    pass

  def _readExistingSpeakerMetadta(self, korpus_path):
    pass
