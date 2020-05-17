import os

import ffmpeg
import pandas as pd
import webrtcvad

from audio_korpora_pipeline.baseobjects import LoggingObject
from audio_korpora_pipeline.inputadapter.audiosplit.splitter import Splitter
from audio_korpora_pipeline.metamodel.mediasession import MediaAnnotationBundle, WrittenResource, MediaFile, \
  MediaSessionActor, Sex, \
  MediaSessionActors, MediaSession


class Adapter(LoggingObject):
  def __init__(self, config):
    super(Adapter, self).__init__()

  def toMetamodel(self) -> MediaSession:
    raise NotImplementedError("Please use a subclass")


class UntranscribedVideoAdapter(Adapter):
  ADAPTERNAME = "UntranscribedVideoAdapter"
  AUDIO_SPLIT_AGRESSIVENESS = 3 #webrtcvad 1 (low), 3 (max)
  mediaAnnotationBundles = []
  mediaSessionActors = set()  # using a set so we don't have duplets

  def __init__(self, config):
    super(UntranscribedVideoAdapter, self).__init__(config=config)
    self.config = config

  def toMetamodel(self):
    self.logger.debug("Untranscribed Video Korpus")
    self._convertVideoToMonoAudio()
    self._splitMonoRawAudioToVoiceSections()

  def _convertVideoToMonoAudio(self):
    self.logger.debug("Extracting audio wav from video")
    in_filename = "./tests/resources/korpora/untranscribed_video/Guetnachtgschichtli/Guetnachtgschichtli-Kater Miro - De Bölle-0164450637.mp4"
    stdout, err = (
      ffmpeg
        .input(in_filename)
        .output('wernutestet.wav', format='wav', acodec='pcm_s16le', ac=1, ar='16k')
        .overwrite_output()
        .run(capture_stdout=True, capture_stderr=True)
    )
    pass

  def _splitMonoRawAudioToVoiceSections(self):
    # use webrtcvad
    audiopath = "wernutestet.wav"

    splitter = Splitter()
    audio, sample_rate = splitter.read_wave("wernutestet.wav")
    vad = webrtcvad.Vad(int(self.AUDIO_SPLIT_AGRESSIVENESS))
    frames = splitter.frame_generator(30, audio, sample_rate)
    frames = list(frames)
    segments = splitter.vad_collector(sample_rate, 30, 300, vad, frames)
    for i, segment in enumerate(segments):
      path = 'chunk-%002d.wav' % (i,)
      print(' Writing %s' % (path,))
      splitter.write_wave(path, segment, sample_rate)

    pass


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
    self.logger.debug("hello archimob input adapter")


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
    self.logger.debug("Created CommonVoice Adapter")
    self.audiofilenames = self._readExistingAudioFiles()
    self.speakermetadata = self._readExistingSpeakerMetadata()
    self._persistMetamodel()
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
    self.mediaAnnotationBundles_dictionary_withoutExtension = {self._getFilenameWithoutExtension(x.identifier): x for x
                                                               in self.mediaAnnotationBundles}
    self.mediaAnnotationBundles_dictionary_withExtension = {self._getFilenameWithExtension(x.identifier): x for x in
                                                            self.mediaAnnotationBundles}
    common_voice_valid_metadata.apply(self._enrichWithTranscriptionInner, axis=1)
    pass

  def _enrichWithTranscriptionInner(self, row):
    currentMediaAnnotationBundle = self.mediaAnnotationBundles_dictionary_withoutExtension.get(row.path,
                                                                                               self.mediaAnnotationBundles_dictionary_withExtension.get(
                                                                                                   row.path))
    currentMediaAnnotationBundle.setWrittenResource(
        WrittenResource(row.sentence, row.client_id, self.LANGUAGECODE_DE))
    currentMediaAnnotationBundle.setMediaFile(MediaFile(row.client_id))
    self.logger.debug(
        "Found matching media-annotation bundle for identifier {} and path {}".format(row.client_id, row.path))

  def _extractMediaSessionActors(self, common_voice_valid_metadata):
    common_voice_valid_metadata.apply(self._createMediaSessionActorFromRow, axis=1)
    self.logger.debug("Found {} Speakers".format(len(self.mediaSessionActors)))

  pass

  def _createMediaSessionActorFromRow(self, row):
    self.mediaSessionActors.add(MediaSessionActor(row.client_id, Sex.toSexEnum(row.gender), row.age))
    pass

  def _getCommonVoiceValidMetadata(self, existing_audio_identifier,
      korpus_path):
    commonvoice_valid_metadatafilenames = ["dev.tsv", "test.tsv", "train.tsv", "validated.tsv"]
    combined_csv = pd.concat(
        [pd.read_csv(os.path.join(korpus_path, f), sep="\t", header=0) for f in commonvoice_valid_metadatafilenames])
    common_voice_valid_metadata = combined_csv[combined_csv.path.isin(existing_audio_identifier)]

    common_voice_valid_metadata = self._fixChangeInDataFormatCommonVoice(common_voice_valid_metadata, combined_csv)

    return common_voice_valid_metadata

  def _getFilenamesFromMediaAnnotationBundles(self):
    return [os.path.splitext(os.path.basename(base.identifier))[0] for base in
            self.mediaAnnotationBundles]

  def _getFilenamesFromMediaAnnotationBundlesWithExtension(self):
    return [os.path.basename(base.identifier) for base in self.mediaAnnotationBundles]

  def _getFilenameWithoutExtension(self, fullpath):
    return os.path.splitext(os.path.basename(fullpath))[0]

  def _getFilenameWithExtension(self, fullpath):
    return os.path.basename(fullpath)

  def _persistMetamodel(self):
    # TODO actual persisting of working json
    # Actual json output
    # print(json.dumps(self.mediaAnnotationBundles, default=lambda o: o.__dict__, sort_keys=True, indent=4))
    pass

  def _buildMediaSession(self):
    actors = MediaSessionActors(self.mediaSessionActors)
    session = MediaSession(self.ADAPTERNAME, actors, self.mediaAnnotationBundles)
    # TODO Validate
    self.mediaSession = session
    pass

  def _fixChangeInDataFormatCommonVoice(self, common_voice_valid_metadata, combined_csv):
    if (len(common_voice_valid_metadata) == 0):
      self.logger.debug(
          "CommonVoice tsv-files seem to have filename-extension set (new fileformat). Trying matching with extension")
      common_voice_valid_metadata = combined_csv[
        combined_csv.path.isin(self._getFilenamesFromMediaAnnotationBundlesWithExtension())]
    self.logger.debug(
        "CommonVoice Valid metadata length is: {}".format(len(common_voice_valid_metadata)))
    return common_voice_valid_metadata
