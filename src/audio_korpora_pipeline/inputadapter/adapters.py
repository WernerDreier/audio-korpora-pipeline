import json
import os

import pandas as pd

from baseobjects import LoggingObject
from metamodel.mediasession import MediaAnnotationBundle, WrittenResource, MediaFile, MediaSessionActor, Sex, \
  MediaSessionActors, MediaSession


class Adapter(LoggingObject):
  def __init__(self, config):
    super(Adapter, self).__init__()

  def toMetamodel(self) -> MediaSession:
    raise NotImplementedError("Please use a subclass")


class ChJugendspracheAdapter(Adapter):
  def __init__(self, config):
    super(ChJugendspracheAdapter, self).__init__(config=config)
    self.config = config

  def toMetamodel(self):
    self.logger.debug("CH-Jugendsprache Korpus")
    # TODO: use the following capabilities to split long audio to spoken-voice chunks (Voice Activation Detection)
    # Use Sox with those parameters:  sox <input.wav> -r 16k -c 1 -b 16 <output.wav>
    # Use webrtcvad#example.py library to chunk the audio


class ArchimobAdapter(Adapter):
  def __init__(self, config):
    super(ArchimobAdapter, self).__init__(config=config)

  def toMetamodel(self):
    self.logger.debug("hello archomob input adapter")


class CommonVoiceAdapter(Adapter):
  RELATIVE_PATH_TO_AUDIO = "clips"
  LANGUAGECODE_DE = "de_DE"
  ADAPTERNAME = "CommonVoiceDE"
  mediaAnnotationBundles = []
  mediaSessionActors = set()  # using a set so we don't have duplets

  def __init__(self, config):
    super(CommonVoiceAdapter, self).__init__(config=config)
    self.config = config

  def toMetamodel(self):
    self.logger.debug("hello CommonVoice Adapter")
    self.audiofilenames = self._readExistingAudioFiles()
    self.speakermetadata = self._readExistingSpeakerMetadata()
    # self._persistMetamodel()
    self._buildMediaSession()
    return self.mediaSession

  def _validateKorpusPath(self):
    korpus_path = self.config['common_voice_input_adapter']['korpus_path']
    if not os.path.isdir(korpus_path):
      raise IOError("Could not read korpus path" + korpus_path)
    return korpus_path

  def _existingAudioFileFullpath(self, filename):
    return os.path.join(self._validateKorpusPath(), self.RELATIVE_PATH_TO_AUDIO, filename)

  def _readExistingAudioFiles(self):
    fullpath = os.path.join(self._validateKorpusPath(), self.RELATIVE_PATH_TO_AUDIO)
    for file in os.listdir(fullpath):
      if file.endswith(".mp3"):
        currentfile = MediaAnnotationBundle(self._existingAudioFileFullpath(file))
        self.mediaAnnotationBundles.append(currentfile)
    self.logger.debug("Found {} audiofiles to process".format(len(self.mediaAnnotationBundles)))
    pass

  def _readExistingSpeakerMetadata(self, ):
    existing_audio_identifier = self._getFilenamesFromMediaAnnotationBundles()
    common_voice_valid_metadata = self._getCommonVoiceValidMetadata(
        existing_audio_identifier, self._validateKorpusPath())

    self._enrichWithTranscription(common_voice_valid_metadata)
    self._extractMediaSessionActors(common_voice_valid_metadata)

  def _enrichWithTranscription(self, common_voice_valid_metadata):
    # TODO will not be very performant
    for index, row in common_voice_valid_metadata.iterrows():
      currentMediaAnnotationBundle = [a for a in self.mediaAnnotationBundles if self._getFilenameWithoutExtension(
          a.identifier) == row.path]
      currentMediaAnnotationBundle[0].setWrittenResource(
          WrittenResource(row.sentence, row.client_id, self.LANGUAGECODE_DE))
      currentMediaAnnotationBundle[0].setMediaFile(MediaFile(row.client_id))

  pass

  def _extractMediaSessionActors(self, common_voice_valid_metadata):
    for index, row in common_voice_valid_metadata.iterrows():
      self.mediaSessionActors.add(MediaSessionActor(row.client_id, Sex.toSexEnum(row.gender), row.age))
    self.logger.debug("Found {} Speakers".format(len(self.mediaSessionActors)))

  pass

  def _getCommonVoiceValidMetadata(self, existing_audio_identifier,
      korpus_path):
    commonvoice_valid_metadatafilenames = ["dev.tsv", "test.tsv", "train.tsv", "validated.tsv"]
    combined_csv = pd.concat(
        [pd.read_csv(os.path.join(korpus_path, f), sep="\t", header=0) for f in commonvoice_valid_metadatafilenames])
    common_voice_valid_metadata = combined_csv[combined_csv.path.isin(existing_audio_identifier)]
    return common_voice_valid_metadata

  def _getFilenamesFromMediaAnnotationBundles(self):
    return [os.path.splitext(os.path.basename(base.identifier))[0] for base in
            self.mediaAnnotationBundles]

  def _getFilenameWithoutExtension(self, fullpath):
    return os.path.splitext(os.path.basename(fullpath))[0]

  def _persistMetamodel(self):
    # TODO actual saving of working json
    # Actual json output
    print(json.dumps(self.mediaAnnotationBundles, default=lambda o: o.__dict__, sort_keys=True, indent=4))
    pass

  def _buildMediaSession(self):
    actors = MediaSessionActors(self.mediaSessionActors)
    session = MediaSession(self.ADAPTERNAME, actors, self.mediaAnnotationBundles)
    # TODO Validate
    self.mediaSession = session
    # print(json.dumps(self.mediaSession, default=lambda o: o.__dict__, sort_keys=True, indent=4))
    print(self.mediaSession)
    pass
