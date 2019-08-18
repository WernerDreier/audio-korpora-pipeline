import os

import pandas as pd

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
    self.speakermetadata = self._readExistingSpeakerMetadata(korpus_path)

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

  def _readExistingSpeakerMetadata(self, korpus_path):

    existing_audio_filenames = self._getFilenamesFromMediaAnnotationBundles()

    commonvoice_valid_metadatafilenames = ["dev.tsv", "test.tsv", "train.tsv",
                                           "validated.tsv"]

    combined_csv = pd.concat(
        [pd.read_csv(os.path.join(korpus_path, f), sep="\t",
                     header=0) for f in commonvoice_valid_metadatafilenames])
    common_voice_valid_metadata = combined_csv[
      combined_csv.path.isin(existing_audio_filenames)]

    # TODO: map common_voice to metadata-structure
    pass

  def _getFilenamesFromMediaAnnotationBundles(self):
    return [os.path.splitext(base.identifier)[0] for base in
            self.mediaAnnotationBundles]
