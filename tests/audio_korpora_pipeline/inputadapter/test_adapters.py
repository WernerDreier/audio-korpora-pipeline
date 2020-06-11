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


class TestArchimobAdapter:

  def test_indicating_1063error(self):
    # given
    config = load_config("config.cfg.sample")
    config_logging(config)
    adapter = ArchimobAdapter(config)

    # assuming this will have all original transcripts ready for testing
    filelist = set(adapter._getAllMediaFilesInBasepath(adapter._validateKorpusPath(), {".wav"}))
    assert any(list(filter(lambda file: os.path.sep + "1063" + os.path.sep + "1063" + os.path.sep in file,
                           filelist))), "We start with some wrong folders in place"

    # when
    assert adapter._fixForDuplicateWavsNecessary(
        filelist), "Should return true, as we expect to have those files within"

  def test_filtering_1063flaw(self):
    # given
    config = load_config("config.cfg.sample")
    config_logging(config)
    adapter = ArchimobAdapter(config)

    # assuming this will have all original transcripts ready for testing
    filelist = set(adapter._getAllMediaFilesInBasepath(adapter._validateKorpusPath(), {".wav"}))
    assert any(list(filter(lambda file: os.path.sep + "1063" + os.path.sep + "1063" + os.path.sep in file,
                           filelist))), "We start with some wrong folders in place"

    # when
    newFilelist = adapter._fixForDuplicateWavs1063(filelist)

    assert (len(newFilelist) < len(filelist)), "It should have filtered something"
    assert adapter._fixForDuplicateWavsNecessary(
        newFilelist) == False, "The new list should not contain any fixable wavs anymore"

  def test_fixing_1083flaw(self):
    # given
    config = load_config("config.cfg.sample")
    config_logging(config)
    adapter = ArchimobAdapter(config)

    # assuming this will have all original transcripts ready for testing
    filelist = set(adapter._getAllMediaFilesInBasepath(adapter._validateKorpusPath(), {".wav"}))
    assert any(list(filter(lambda file: "1082_2d1082_2_TLI_3.wav" in file,
                           filelist))), "We start with some wrong folders in place"

    # when
    newFilelist = adapter._fixForWrongFilenames1082(filelist)

    assert (len(newFilelist) == len(filelist)), "It should have same length entries"
    assert (newFilelist != filelist), "It should have changed something"
    assert adapter._fixForWrongFilenamesNecessary(
        newFilelist) == False, "The new list should not contain any fixable wavs anymore"
