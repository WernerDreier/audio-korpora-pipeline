import glob
import glob
import os

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


class TestUntranscribedMediaSplitterAdapter:

  def touch(self, path):
    with open(path, 'a'):
      os.utime(path, None)


class TestUntranscribedVideoAdapter:

  def setup_method(self, method):
    # clearWorkingDirs()
    print("setup")

  def test_video_returns_media_session(self):
    # given
    config = load_config("config.cfg.sample")
    config_logging(config)
    adapter = UntranscribedVideoAdapter(config)
    # when
    metamodel = adapter.toMetamodel()
    # then
    assert len(metamodel.mediaSessionActors) == 1, "Muss genau einen Speaker (Unknown) enthalten"
    assert metamodel.mediaSessionActors.pop().id == "UNKNOWN", "Muss genau einen Speaker (Unknown) enthalten"
    assert len(metamodel.mediaAnnotationBundles) > 2, "Muss mehr als ein Media bundle enthalten"
