import contextlib
import glob
import os
import wave

from audio_korpora_pipeline.inputadapter.adapters import UntranscribedVideoAdapter, ChJugendspracheAdapter, \
  ArchimobAdapter
from audio_korpora_pipeline.utils import load_config, config_logging


def clearWorkingDirs():
  config = load_config("config.cfg.sample")
  config_logging(config)
  adapters = [UntranscribedVideoAdapter(config), ChJugendspracheAdapter(config), ArchimobAdapter(config)]
  korpusPaths = [adapter._validateKorpusPath() for adapter in adapters]

  for korpusPath in korpusPaths:
    for filename in glob.glob(os.path.join(korpusPath, "**", "*chunk*.wav"), recursive=True):
      print("Triggered deleting files for folder {}".format(filename))
      os.remove(filename)
    for filename in glob.glob(os.path.join(korpusPath, "**", "*.mono.wav"), recursive=True):
      print("Triggered deleting files for folder {}".format(filename))
      os.remove(filename)


class TestUntranscribedVideoAdapter:

  def setup_method(self, method):
    clearWorkingDirs()

  def test_untranscribed_extract_audio_from_video(self):
    # given
    config = load_config("config.cfg.sample")
    config_logging(config)
    adapter = UntranscribedVideoAdapter(config)
    korpusPath = adapter._validateKorpusPath()  # assuming this function works as expected
    assert os.path.exists(os.path.join(korpusPath, "1 gegen 100",
                                       "1 gegen 100-1 gegen 100 – Jahresrückblick mit Angélique Beldner-0943170628.mp4"))
    assert os.path.exists(
        os.path.join(korpusPath, "Guetnachtgschichtli", "Guetnachtgschichtli-Kater Miro - De Bölle-0164450637.mp4"))
    # when
    wavFilenames = adapter._convertMediafileToMonoAudio(korpusPath, ".mp4")
    # then
    assert len(wavFilenames) > 0
    assert os.path.exists(os.path.join(korpusPath, "1 gegen 100",
                                       "1 gegen 100-1 gegen 100 – Jahresrückblick mit Angélique Beldner-0943170628.mono.wav")), "Erstes Video sollte in Wav gewandelt worden sein"
    assert os.path.exists(os.path.join(korpusPath, "Guetnachtgschichtli",
                                       "Guetnachtgschichtli-Kater Miro - De Bölle-0164450637.mono.wav")), "Zweites Video sollte in Wav gewandelt worden sein"

  def test_untranscribed_extract_split_audio(self):
    # given
    config = load_config("config.cfg.sample")
    config_logging(config)
    adapter = UntranscribedVideoAdapter(config)
    korpusPath = adapter._validateKorpusPath()  # assuming this function works as expected
    adapter._convertMediafileToMonoAudio(korpusPath, ".mp4")  # create mono wavs full length
    wavFilenames = [os.path.join(korpusPath, "1 gegen 100",
                                 "1 gegen 100-1 gegen 100 – Jahresrückblick mit Angélique Beldner-0943170628.mono.wav"),
                    os.path.join(korpusPath, "Guetnachtgschichtli",
                                 "Guetnachtgschichtli-Kater Miro - De Bölle-0164450637.mono.wav")]
    assert os.path.exists(wavFilenames[0]), "Wav basefile 1 must exist"
    assert os.path.exists(wavFilenames[1]), "Wav basefile 2 must exist"
    # when
    adapter._splitMonoRawAudioToVoiceSections(wavFilenames)
    # then
    # assert basefile is deleted
    assert not (os.path.exists(wavFilenames[0])), "Wav basefile 1 must NOT exist anymore"
    # assert length is in between 2 and 18 seconds
    with os.scandir(os.path.join(korpusPath, "1 gegen 100")) as it:
      for entry in it:
        if entry.name.endswith(".wav") and entry.is_file():
          print(entry.name, entry.path)
          with contextlib.closing(wave.open(entry.path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            assert duration > 1, "Every audio chunk must be at least 2 seconds long"
            assert duration < 19, "Every audio chunk must be at most 18 seconds long"


class TestChJugendspracheAdapter:

  def setup_method(self, method):
    clearWorkingDirs()

  def test_ch_jugendsprache_extract_audio_from_long_audio_files(self):
    # given
    config = load_config("config.cfg.sample")
    config_logging(config)
    adapter = ChJugendspracheAdapter(config)
    korpusPath = adapter._validateKorpusPath()  # assuming this function works as expected
    assert os.path.exists(os.path.join(korpusPath, "S2-Pascal Hager", "SNF_jspr_I4_S2_Hager_060912_4.WAV"))
    assert os.path.exists(os.path.join(korpusPath, "S2-Pascal Hager", "SNF_jspr_I4_S2_Hager_061218_16a.WAV"))
    # when
    wavFilenames = adapter._convertMediafileToMonoAudio(korpusPath, ".WAV")
    # then
    assert len(wavFilenames) > 0
    assert os.path.exists(os.path.join(korpusPath, "S2-Pascal Hager",
                                       "SNF_jspr_I4_S2_Hager_060912_4.mono.wav")), "Erstes Audio sollte in Wav gewandelt worden sein"
    assert os.path.exists(os.path.join(korpusPath, "S2-Pascal Hager",
                                       "SNF_jspr_I4_S2_Hager_061218_16a.mono.wav")), "Zweites Audio sollte in Wav gewandelt worden sein"

  def test_ch_jugendsprache_split_long_audio_files(self):
    # given
    config = load_config("config.cfg.sample")
    config_logging(config)
    adapter = ChJugendspracheAdapter(config)
    korpusPath = adapter._validateKorpusPath()  # assuming this function works as expected
    adapter._convertMediafileToMonoAudio(korpusPath, ".WAV")  # create mono wavs full length
    wavFilenames = [os.path.join(korpusPath, "S2-Pascal Hager", "SNF_jspr_I4_S2_Hager_060912_4.mono.wav"),
                    os.path.join(korpusPath, "S2-Pascal Hager", "SNF_jspr_I4_S2_Hager_061218_16a.mono.wav")]
    assert os.path.exists(wavFilenames[0]), "Wav basefile 1 must exist"
    assert os.path.exists(wavFilenames[1]), "Wav basefile 2 must exist"
    # when
    adapter._splitMonoRawAudioToVoiceSections(wavFilenames)
    # then
    # assert basefile is deleted
    assert not (os.path.exists(wavFilenames[0])), "Wav basefile 1 must NOT exist anymore"
    # assert length is in between 2 and 18 seconds
    with os.scandir(os.path.join(korpusPath, "S2-Pascal Hager")) as it:
      for entry in it:
        if entry.name.endswith(".mono.wav") and entry.is_file():
          print(entry.name, entry.path)
          with contextlib.closing(wave.open(entry.path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            assert duration > 1, "Every audio chunk must be at least 2 seconds long"
            assert duration < 19, "Every audio chunk must be at most 18 seconds long"

  def test_ch_jugendsprache_returns_media_session(self):
    # given
    config = load_config("config.cfg.sample")
    config_logging(config)
    adapter = ChJugendspracheAdapter(config)
    # when
    metamodel = adapter.toMetamodel()
    # then
    assert len(metamodel.mediaSessionActors) == 1, "Muss genau einen Speaker (Unknown) enthalten"
    assert metamodel.mediaSessionActors.pop().id == "UNKNOWN", "Muss genau einen Speaker (Unknown) enthalten"
    assert len(metamodel.mediaAnnotationBundles) > 2, "Muss mehr als ein Media bundle enthalten"


class TestArchimobAdapter:

  def setup_method(self, method):
    clearWorkingDirs()

  def test_archimob_extract_audio_from_long_audio_files(self):
    # given
    config = load_config("config.cfg.sample")
    config_logging(config)
    adapter = ArchimobAdapter(config)
    korpusPath = adapter._validateKorpusPath()  # assuming this function works as expected
    assert os.path.exists(os.path.join(korpusPath, "christof", "audio_segmented_anonymized", "1044", "d1044_T1245.wav"))
    assert os.path.exists(
        os.path.join(korpusPath, "christof", "audio_segmented_anonymized", "1083_2", "d1083_2_TLI_51.wav"))
    # when
    wavFilenames = adapter._convertMediafileToMonoAudio(korpusPath, ".wav")
    # then
    assert len(wavFilenames) > 0
    assert os.path.exists(os.path.join(korpusPath, "christof", "audio_segmented_anonymized", "1044",
                                       "d1044_T1245.mono.wav")), "Erstes Audio sollte in Wav gewandelt worden sein"
    assert os.path.exists(os.path.join(korpusPath, "christof", "audio_segmented_anonymized", "1083_2",
                                       "d1083_2_TLI_51.mono.wav")), "Zweites Audio sollte in Wav gewandelt worden sein"

  def test_archimob_returns_media_session(self):
    # given
    config = load_config("config.cfg.sample")
    config_logging(config)
    adapter = ArchimobAdapter(config)
    # when
    metamodel = adapter.toMetamodel()
    # then
    assert len(metamodel.mediaSessionActors) == 1, "Muss genau einen Speaker (Unknown) enthalten"
    assert metamodel.mediaSessionActors.pop().id == "UNKNOWN", "Muss genau einen Speaker (Unknown) enthalten"
    assert len(metamodel.mediaAnnotationBundles) > 2, "Muss mehr als ein Media bundle enthalten"
