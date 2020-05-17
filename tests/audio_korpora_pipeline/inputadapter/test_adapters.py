from audio_korpora_pipeline.inputadapter.adapters import UntranscribedVideoAdapter
from audio_korpora_pipeline.utils import load_config, config_logging


def test_untranscribed_extract_audio():
  # given
  config = load_config("config.cfg.sample")
  config_logging(config)
  adapter = UntranscribedVideoAdapter(config)
  adapter.toMetamodel()


  # when
  # then
