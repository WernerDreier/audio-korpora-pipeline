import contextlib
import os
import wave

from audio_korpora_pipeline.inputadapter.adapters import UntranscribedVideoAdapter, ChJugendspracheAdapter
from audio_korpora_pipeline.utils import load_config, config_logging


def test_untranscribed_extract_audio_from_video():
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
  wavFilenames = adapter._convertMediafileToMonoAudio()
  # then
  assert len(wavFilenames) > 0
  assert os.path.exists(os.path.join(korpusPath, "1 gegen 100",
                                     "1 gegen 100-1 gegen 100 – Jahresrückblick mit Angélique Beldner-0943170628.wav")), "Erstes Video sollte in Wav gewandelt worden sein"
  assert os.path.exists(os.path.join(korpusPath, "Guetnachtgschichtli",
                                     "Guetnachtgschichtli-Kater Miro - De Bölle-0164450637.wav")), "Zweites Video sollte in Wav gewandelt worden sein"


def test_untranscribed_extract_split_audio():
  # given
  config = load_config("config.cfg.sample")
  config_logging(config)
  adapter = UntranscribedVideoAdapter(config)
  korpusPath = adapter._validateKorpusPath()  # assuming this function works as expected
  wavFilenames = [os.path.join(korpusPath, "1 gegen 100",
                               "1 gegen 100-1 gegen 100 – Jahresrückblick mit Angélique Beldner-0943170628.wav"),
                  os.path.join(korpusPath, "Guetnachtgschichtli",
                               "Guetnachtgschichtli-Kater Miro - De Bölle-0164450637.wav")]
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


def test_ch_jugendsprache_extract_audio_from_long_audio_files():
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


def test_ch_jugendsprache_split_long_audio_files():
  # given
  config = load_config("config.cfg.sample")
  config_logging(config)
  adapter = ChJugendspracheAdapter(config)
  korpusPath = adapter._validateKorpusPath()  # assuming this function works as expected
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
