from audio_korpora_pipeline.inputadapter.adapters import UntranscribedVideoAdapter
from audio_korpora_pipeline.utils import load_config, config_logging
import os


def test_untranscribed_extract_audio_from_video():
  # given
  config = load_config("config.cfg.sample")
  config_logging(config)
  adapter = UntranscribedVideoAdapter(config)
  korpusPath = adapter._validateKorpusPath() #assuming this function works as expected
  assert(os.path.exists(os.path.join(korpusPath,"1 gegen 100","1 gegen 100-1 gegen 100 – Jahresrückblick mit Angélique Beldner-0943170628.mp4")))
  assert(os.path.exists(os.path.join(korpusPath,"Guetnachtgschichtli","Guetnachtgschichtli-Kater Miro - De Bölle-0164450637.mp4")))
  # when
  wavFilenames = adapter._convertVideoToMonoAudio()
  # then
  assert(len(wavFilenames) > 0)
  assert(os.path.exists(os.path.join(korpusPath,"1 gegen 100","1 gegen 100-1 gegen 100 – Jahresrückblick mit Angélique Beldner-0943170628.wav")),"Erstes Video sollte in Wav gewandelt worden sein")
  assert(os.path.exists(os.path.join(korpusPath,"Guetnachtgschichtli","Guetnachtgschichtli-Kater Miro - De Bölle-0164450637.wav")),"Zweites Video sollte in Wav gewandelt worden sein")


