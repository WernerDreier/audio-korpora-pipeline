import contextlib
import wave

import librosa

from audio_korpora_pipeline.inputadapter.adapters import UntranscribedVideoAdapter
from audio_korpora_pipeline.utils import load_config, config_logging
import os


def test_untranscribed_extract_audio_from_video():
  # given
  config = load_config("config.cfg.sample")
  config_logging(config)
  adapter = UntranscribedVideoAdapter(config)
  korpusPath = adapter._validateKorpusPath() #assuming this function works as expected
  assert os.path.exists(os.path.join(korpusPath,"1 gegen 100","1 gegen 100-1 gegen 100 – Jahresrückblick mit Angélique Beldner-0943170628.mp4"))
  assert os.path.exists(os.path.join(korpusPath,"Guetnachtgschichtli","Guetnachtgschichtli-Kater Miro - De Bölle-0164450637.mp4"))
  # when
  wavFilenames = adapter._convertVideoToMonoAudio()
  # then
  assert len(wavFilenames) > 0
  assert os.path.exists(os.path.join(korpusPath,"1 gegen 100","1 gegen 100-1 gegen 100 – Jahresrückblick mit Angélique Beldner-0943170628.wav")),"Erstes Video sollte in Wav gewandelt worden sein"
  assert os.path.exists(os.path.join(korpusPath,"Guetnachtgschichtli","Guetnachtgschichtli-Kater Miro - De Bölle-0164450637.wav")),"Zweites Video sollte in Wav gewandelt worden sein"

def test_untranscribed_extract_split_audio():
  # given
  config = load_config("config.cfg.sample")
  config_logging(config)
  adapter = UntranscribedVideoAdapter(config)
  korpusPath = adapter._validateKorpusPath() #assuming this function works as expected
  wavFilenames = [os.path.join(korpusPath,"1 gegen 100","1 gegen 100-1 gegen 100 – Jahresrückblick mit Angélique Beldner-0943170628.wav"),
                  os.path.join(korpusPath,"Guetnachtgschichtli","Guetnachtgschichtli-Kater Miro - De Bölle-0164450637.wav")]
  assert os.path.exists(wavFilenames[0]), "Wav basefile 1 must exist"
  assert os.path.exists(wavFilenames[1]),"Wav basefile 2 must exist"
  # when
  adapter._splitMonoRawAudioToVoiceSections(wavFilenames)
  # then
  #assert basefile is deleted
  assert not(os.path.exists(wavFilenames[0])), "Wav basefile 1 must NOT exist anymore"
  #assert length is in between 2 and 18 seconds
  with os.scandir(os.path.join(korpusPath,"1 gegen 100")) as it:
    for entry in it:
      if entry.name.endswith(".wav") and entry.is_file():
        print(entry.name, entry.path)
        with contextlib.closing(wave.open(entry.path,'r')) as f:
          frames = f.getnframes()
          rate = f.getframerate()
          duration = frames / float(rate)
          assert duration > 1, "Every audio chunk must be at least 2 seconds long"
          assert duration < 19, "Every audio chunk must be at most 18 seconds long"






