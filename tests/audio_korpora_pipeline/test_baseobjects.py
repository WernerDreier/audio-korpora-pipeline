from audio_korpora_pipeline.baseobjects import FileHandlingObject


class TestFileHandlingObject:

  def test_finding_filenamepart_split(self):
    # given
    filenamepart = ".mono.wav"
    filelist = ["audio1.wav", "audio1.mono.wav", "audio2.wav", "audio2.mono.wav", "audio3.wav", "audio4.NOWAV",
                "audio4.mono.NOWAV"]
    handlingThing = FileHandlingObject()
    # when
    filesContainingFilenamepart, filesNotContainingFilenamepart = handlingThing._filterFilesNamedLikeTheFilenamepart(
        filelist, filenamepart)
    # then
    print("Not containing filenamepart {}".format(filesNotContainingFilenamepart))
    print("Containing filenamepart {}".format(filesContainingFilenamepart))
    assert len(filesNotContainingFilenamepart) == 5, "Must have exactly 5 items"
    assert set(filesContainingFilenamepart).isdisjoint(
        set(filesNotContainingFilenamepart)), "Sets cannot contain same elements"

  def test_finding_processed_files(self):
    # given
    filenamepart = ".mono.wav"
    containingfilenamepart = ["audio1.mono.wav", "audio2.mono.wav"]
    notContainingfilenamepart = ["audio1.wav", "audio2.wav", "audio3.wav", "audio4.NOWAV", "audio4.mono.NOWAV",
                                 "audio5.wav"]
    shouldBeMarkedAsProcessed = {'audio1.mono.wav', 'audio2.mono.wav', 'audio2.wav', 'audio1.wav'}
    shouldBeMarkedAsUnprocessed = {'audio4.NOWAV', 'audio4.mono.NOWAV', 'audio5.wav', 'audio3.wav'}
    handlingThing = FileHandlingObject()
    # when
    processedFiles, unprocessedFiles = handlingThing._filterOriginalFilesIfFileWithFilenamepartIsPresent(
        containingfilenamepart,
        notContainingfilenamepart, filenamepart)
    # then
    print("\n\nProcessedFiles are {}".format(processedFiles))
    print("Unprocessed are {}".format(unprocessedFiles))
    assert len(processedFiles) == len(shouldBeMarkedAsProcessed), "Must have exactly {} items".format(
        len(shouldBeMarkedAsProcessed))
    assert set(processedFiles).isdisjoint(
        set(unprocessedFiles)), "Sets cannot contain same elements"
    assert shouldBeMarkedAsProcessed == set(processedFiles), "Processed files do not match"
    assert shouldBeMarkedAsUnprocessed == set(unprocessedFiles), "Unprocessed files do not match"

  def test_stability_for_None_Inputs(self):
    # given
    filenamepart = ""
    containingfilenamepart = None
    notContainingfilenamepart = None
    handlingThing = FileHandlingObject()
    # when
    processedFiles, unprocessedFiles = handlingThing._filterOriginalFilesIfFileWithFilenamepartIsPresent(
        containingfilenamepart,
        notContainingfilenamepart, filenamepart)
    # then
    print("\n\nProcessedFiles are {}".format(processedFiles))
    print("Unprocessed are {}".format(unprocessedFiles))

  def test_processed_files_leaving_originals(self):
    # given
    filenamepart = ".mono.wav"
    filelist = ["audio1.mono.wav", "audio2.mono.wav", "audio1.wav", "audio2.wav", "audio3.wav", "audio4.NOWAV",
                "audio4.mono.NOWAV",
                "audio5.wav"]
    shouldBeMarkedAsProcessed = {'audio1.mono.wav', 'audio2.mono.wav'}
    shouldBeMarkedAsUnprocessed = {'audio4.NOWAV', 'audio4.mono.NOWAV', 'audio5.wav', 'audio3.wav', 'audio2.wav',
                                   'audio1.wav'}
    handlingThing = FileHandlingObject()
    # when
    processedFiles, unprocessedFiles = handlingThing.filterAudioFilesContainingNamePattern(filelist, filenamepart,
                                                                                           skipAlreadyProcessedFiles=False)
    # then
    print("\n\nProcessedFiles are {}".format(processedFiles))
    print("Unprocessed are {}".format(unprocessedFiles))
    assert len(processedFiles) == len(shouldBeMarkedAsProcessed), "Must have exactly {} items".format(
        len(shouldBeMarkedAsProcessed))
    assert set(processedFiles).isdisjoint(
        set(unprocessedFiles)), "Sets cannot contain same elements"
    assert shouldBeMarkedAsProcessed == set(processedFiles), "Processed files do not match"
    assert shouldBeMarkedAsUnprocessed == set(unprocessedFiles), "Unprocessed files do not match"

  def test_processed_files_removing_originals(self):
    # given
    filenamepart = ".mono.wav"
    filelist = ["audio1.mono.wav", "audio2.mono.wav", "audio1.wav", "audio2.wav", "audio3.wav", "audio4.NOWAV",
                "audio4.mono.NOWAV",
                "audio5.wav"]
    shouldBeMarkedAsProcessed = {'audio1.mono.wav', 'audio2.mono.wav', 'audio2.wav', 'audio1.wav'}
    shouldBeMarkedAsUnprocessed = {'audio4.NOWAV', 'audio4.mono.NOWAV', 'audio5.wav', 'audio3.wav', }
    handlingThing = FileHandlingObject()
    # when
    processedFiles, unprocessedFiles = handlingThing.filterAudioFilesContainingNamePattern(filelist, filenamepart,
                                                                                           skipAlreadyProcessedFiles=True)
    # then
    print("\n\nProcessedFiles are {}".format(processedFiles))
    print("Unprocessed are {}".format(unprocessedFiles))
    assert len(processedFiles) == len(shouldBeMarkedAsProcessed), "Must have exactly {} items".format(
        len(shouldBeMarkedAsProcessed))
    assert set(processedFiles).isdisjoint(
        set(unprocessedFiles)), "Sets cannot contain same elements"
    assert shouldBeMarkedAsProcessed == set(processedFiles), "Processed files do not match"
    assert shouldBeMarkedAsUnprocessed == set(unprocessedFiles), "Unprocessed files do not match"
