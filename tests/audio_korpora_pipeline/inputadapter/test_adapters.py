import glob
import glob
import os

from pandas import DataFrame

from audio_korpora_pipeline.inputadapter.adapters import UntranscribedVideoAdapter, ChJugendspracheAdapter, \
  ArchimobAdapter, SwissText2020LowresourceTask
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
    assert adapter._fixForDuplicateWavs1063Necessary(
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
    assert adapter._fixForDuplicateWavs1063Necessary(
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
    assert adapter._fixForWrongFilenames1082Necessary(
        newFilelist) == False, "The new list should not contain any fixable wavs anymore"

  def test_full_transcription_of_one_file(self):
    # given
    config = load_config("config.cfg.sample")
    config_logging(config)
    adapter = ArchimobAdapter(config)
    fileToConvert = os.path.join(adapter._validateKorpusPath(), "Archimob_Release_2", "1007.xml")

    expectedOutputSentenceContainingPauseAndVocal = "#ehm s ich bin am sächsezwänzgischte jänner nünzehundertzwölf @ gibore"
    expectedOutputSentenceContainingUnclear = "maitschi und de"
    expectedOutputSentenceContainingDeletion = "de he det hend"
    expectedOutputSentenceContainingGap = "d1007-T62"

    # when
    transcriptionForThisSpeaker = adapter._extractSingleXmlFileThread(fileToConvert)

    # then
    assert len(
        transcriptionForThisSpeaker) == 3, "Format should be: result(bool), filename(str), transcriptions(dataframe)"
    assert transcriptionForThisSpeaker[0] == True, "Should have successfully parsed"
    assert transcriptionForThisSpeaker[1] == fileToConvert, "Filename should be the same as inputted"
    assert "chönd sii" == (transcriptionForThisSpeaker[2]).loc[
      0, "transcript"], "Some example for correct transcription"

    transcript = (transcriptionForThisSpeaker[2])

    assert expectedOutputSentenceContainingPauseAndVocal == transcript[
      transcript.Filename == "d1007-T5"].iloc[0]["transcript"], "Output sentence does not look like it should"
    assert expectedOutputSentenceContainingUnclear in transcript[
      transcript.Filename == "d1007-T40"].iloc[0]["transcript"], "Output sentence does not contain unclear word"
    assert expectedOutputSentenceContainingDeletion in transcript[
      transcript.Filename == "d1007-T977"].iloc[0]["transcript"], "Output sentence does not containg deletion"

    assert expectedOutputSentenceContainingGap not in set(
        (transcriptionForThisSpeaker[2])["Filename"]), "Should not contain known sentence with <gap> tag"

  def test_full_transcription_of_two_files(self):
    # given
    config = load_config("config.cfg.sample")
    config_logging(config)
    adapter = ArchimobAdapter(config)
    fileToConvert1 = os.path.join(adapter._validateKorpusPath(), "Archimob_Release_2", "1007.xml")
    fileToConvert2 = os.path.join(adapter._validateKorpusPath(), "Archimob_Release_2", "1082_2.xml")

    # when
    extraction = adapter._extract([fileToConvert1, fileToConvert2])

    # then
    print(extraction)
    assert len(extraction) == 2, "Should have two speaker tuples back"
    assert len(extraction[0]) == 2, "Should have a tuple back"
    assert extraction[0][0] == fileToConvert1 or extraction[0][
      0] == fileToConvert2, "Should have file one or two set as origin"
    assert type(extraction[0][1]) == DataFrame, "Should have a frame bcak"
    assert {'Filename', 'transcript'}.issubset(
        extraction[0][1].columns), "Columns of frame should be filename and transcript"

  def test_transcription_plus_other(self):
    # given
    config = load_config("config.cfg.sample")
    config_logging(config)
    adapter = ArchimobAdapter(config)
    fileToConvert1 = os.path.join(adapter._validateKorpusPath(), "Archimob_Release_2", "1007.xml")
    fileToConvert2 = os.path.join(adapter._validateKorpusPath(), "Archimob_Release_2", "1044.xml")
    filelist = set(adapter._getAllMediaFilesInBasepath(adapter._validateWorkdir(),
                                                       {".wav"}))  # assuming wav generation was done properly
    transcriptions = adapter._extract([fileToConvert1, fileToConvert2])  # assuming this works as expected

    # when
    versa = adapter._onlyTranscriptionsWithMediaFilesAndViceVersa(transcriptions, filelist)
    bundles = adapter._createActualMediaAnnotationBundles(versa)

    # then
    assert {'FullpathFilename', 'transcript'}.issubset(
        versa.columns), "Columns of frame should be FilenameFullpath and transcript"

    print(bundles)

  def test_integration_test_archimob_input(self):
    # given
    config = load_config("config.cfg.sample")
    config_logging(config)
    adapter = ArchimobAdapter(config)

    # when
    mediaSession = adapter.toMetamodel()

    # then
    print(mediaSession)


class TestSwisstext2020:
  def test_integration_test_swisstext2020_input(self):
    # given
    config = load_config("config.cfg.sample")
    config_logging(config)
    adapter = SwissText2020LowresourceTask(config)

    # when
    mediaSession = adapter.toMetamodel()

    # then
    print(mediaSession)
