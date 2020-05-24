import shutil

from audio_korpora_pipeline.inputadapter.adapters import ChJugendspracheAdapter
from audio_korpora_pipeline.outputadapter.adapters import FairseqWav2VecAdapter
from audio_korpora_pipeline.utils import load_config, config_logging


def clearWorkingDirs():
  print("Cleaning working dirs")
  config = load_config("config.cfg.sample")
  config_logging(config)
  adapter = FairseqWav2VecAdapter(config)
  korpusPath = adapter._basePath()
  shutil.rmtree(korpusPath, ignore_errors=True)


class TestFairseqWav2VecAdapter:

  def setup_method(self, method):
    clearWorkingDirs()

  def test_from_metamodel_integration_test(self):
    # given
    config = load_config("config.cfg.sample")
    config_logging(config)
    inputAdapter = ChJugendspracheAdapter(config)
    metamodel = inputAdapter.toMetamodel()
    assert len(metamodel.mediaSessionActors) == 1, "Muss genau einen Speaker (Unknown) enthalten"
    assert metamodel.mediaSessionActors.pop().id == "UNKNOWN", "Muss genau einen Speaker (Unknown) enthalten"
    assert len(metamodel.mediaAnnotationBundles) > 2, "Muss mehr als ein Media bundle enthalten"
    outputAdapter = FairseqWav2VecAdapter(config)
    # when
    outputAdapter.fromMetamodel(metamodel)
    # then
    # TODO check for proper output programatically
