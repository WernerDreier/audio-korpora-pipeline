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


def _clearWorkingDirs():
  print("Cleaning working dirs")
  config = load_config("config.cfg.sample")
  config_logging(config)
  clearWorkingDirsInput(config)
  adapter = FairseqWav2VecAdapter(config)
  korpusPath = adapter._basePath()
  shutil.rmtree(korpusPath, ignore_errors=True)


def test_clearWorkingDirs():
  _clearWorkingDirs()


class TestFairseqWav2VecAdapter:

  def setup_method(self, method):
    print("Setup triggered")

  def test_from_metamodel_integration_test(self):
    # given
    _clearWorkingDirs()  # Clear directories
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

  def test_small_integration_test_with_everything_already_in_place(self):
    # given
    # assuming test before has been run successfully and files are not deleted
    config = load_config("config.cfg.sample")
    config_logging(config)

    inputAdapters = _createInputAdapters(config, ExistingInputAdapter.UNTRANSCRIBED_VIDEO.value)
    outputAdapters = _createOutputAdapters(config, ExistingOutputAdapter.FAIRSEQ_WAV2VEC.value)
    # when
    metamodels = _transformInputsToMetamodel(inputAdapters)
    outputs = _transformMetamodelsToOutputs(metamodels, outputAdapters)
    # then
    # TODO check for proper output programatically, atm done manually

  def test_validate_tsv(self):
    # given
    allExistingWavsInTargetFolder = [
      "1 gegen 100-1 gegen 100 – Jahresrückblick mit Angélique Beldner-0943170628_chunk_00014.wav",
      "1 gegen 100-1 gegen 100 – Jahresrückblick mit Angélique Beldner-0943170628_chunk_00016.wav",
      "shouldnetbeHere_butignored.wav"]

    config = load_config("config.cfg.sample")
    config_logging(config)
    outputAdapter = FairseqWav2VecAdapter(config)
    self._createDummyFileToValidate(outputAdapter._validateBasePath())
    # when
    filesToProcess = outputAdapter._validate_tsv_file(allExistingWavsInTargetFolder, "dummy.tsv", 16000)
    # then
    print(filesToProcess)

  def _createDummyFileToValidate(self, path):
    f = open(os.path.join(path, "dummy.tsv"), "w", encoding="UTF-8", newline="\n")
    f.write(
        "C:\\dev\\datascience-repositories\\audio_korpora_pipeline\\tests\\resources\\korpora\\output\\fairseqWav2Vec\\wavs\n")
    f.write("1 gegen 100-1 gegen 100 – Jahresrückblick mit Angélique Beldner-0943170628_chunk_00014.wav\t121920\n")
    f.write("I am not copied correctly.wav	121920\n")
    f.write("1 gegen 100-1 gegen 100 – Jahresrückblick mit Angélique Beldner-0943170628_chunk_00016.wav\t68123")
    f.close()


class TestOpenSeq2SeqAdapter:
  def test_small_integration_test_with_everything_already_in_place(self):
    # given
    # assuming test before has been run successfully and files are not deleted
    config = load_config("config.cfg.sample")
    config_logging(config)

    inputAdapters = _createInputAdapters(config, ExistingInputAdapter.ARCHIMOB.value)
    outputAdapters = _createOutputAdapters(config, ExistingOutputAdapter.OPENSEQ2SEQ.value)
    # when
    metamodels = _transformInputsToMetamodel(inputAdapters)
    outputs = _transformMetamodelsToOutputs(metamodels, outputAdapters)
