import glob
import os
import shutil

from audio_korpora_pipeline.audio_korpora_pipeline import ExistingInputAdapter, ExistingOutputAdapter
from audio_korpora_pipeline.cli import _createInputAdapters, _transformInputsToMetamodel, _transformMetamodelsToOutputs, \
  _createOutputAdapters
from audio_korpora_pipeline.inputadapter.adapters import UntranscribedVideoAdapter, ChJugendspracheAdapter, \
  ArchimobAdapter
from audio_korpora_pipeline.outputadapter.adapters import FairseqWav2VecAdapter
from audio_korpora_pipeline.utils import load_config, config_logging


def clearWorkingDirsInput(config):
  adapters = [UntranscribedVideoAdapter(config), ChJugendspracheAdapter(config), ArchimobAdapter(config)]
  korpusPaths = [adapter._validateKorpusPath() for adapter in adapters]

  for korpusPath in korpusPaths:
    for filename in glob.glob(os.path.join(korpusPath, "**", "*chunk*.wav"), recursive=True):
      print("Triggered deleting files for folder {}".format(filename))
      os.remove(filename)
    for filename in glob.glob(os.path.join(korpusPath, "**", "*.mono.wav"), recursive=True):
      print("Triggered deleting files for folder {}".format(filename))
      os.remove(filename)


def clearWorkingDirs():
  print("Cleaning working dirs")
  config = load_config("config.cfg.sample")
  config_logging(config)
  clearWorkingDirsInput(config)
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

    inputAdapters = _createInputAdapters(config,
                                         ExistingInputAdapter.ARCHIMOB.value + "," +
                                         ExistingInputAdapter.CH_JUGENDSPRACHE.value + "," +
                                         ExistingInputAdapter.UNTRANSCRIBED_VIDEO.value)
    outputAdapters = _createOutputAdapters(config, ExistingOutputAdapter.FAIRSEQ_WAV2VEC.value)
    # when
    metamodels = _transformInputsToMetamodel(inputAdapters)
    outputs = _transformMetamodelsToOutputs(metamodels, outputAdapters)
    # then
    # TODO check for proper output programatically, atm done manually
