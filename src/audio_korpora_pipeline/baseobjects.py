import json
import logging
import os


class LoggingObject(object):
  def __init__(self):
    self.logger = logging.getLogger(__name__)

  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__,
                      sort_keys=True, indent=4)

  """A mixin implementing a simple __repr__."""

  def __repr__(self):
    return "<{klass} {attrs}>".format(
        klass=self.__class__.__name__,
        attrs=" ".join("{}={!r}".format(k, v) for k, v in self.__dict__.items()),
    )

  def __hash__(self):
    return hash(self.__repr__())


class FileHandlingObject(LoggingObject):
  def __init__(self):
    super(FileHandlingObject, self).__init__()

  def filterFilesAlreadyBeingTransformed(self, filelist, originalFilenamePattern, transformedFilenamepattern,
      skipAlreadyProcessedFiles=True):
    processedFiles = []
    unprocessedFiles = []
    filesContainingFilenamepart, filesNotContainingFilenamepart = self._filterFilesNamedLikeFilenamepattern(filelist,
                                                                                                            transformedFilenamepattern)

    if (skipAlreadyProcessedFiles):
      self.logger.debug("Will remove original files from list too")
      processedFiles, unprocessedFiles = self._filterOriginalFilesIfFileWithFilenamepartIsPresent(
          filesContainingFilenamepart, filesNotContainingFilenamepart, transformedFilenamepattern,
          originalFilenamePattern)
    else:
      processedFiles = filesContainingFilenamepart
      unprocessedFiles = filesNotContainingFilenamepart

    self.logger.debug(
        "Got {} files to process and {} already processed for filenamepart {} for initial list of length {}".format(
            len(unprocessedFiles), len(processedFiles), transformedFilenamepattern, len(filelist)))
    return processedFiles, unprocessedFiles

  def _filterFilesNamedLikeFilenamepattern(self, filelist, filenamepart):
    filesContainingFilenamepart = []
    filesNotContainingFilenamepart = []
    for file in filelist:
      if (filenamepart in file):
        filesContainingFilenamepart.append(file)
        self.logger.info(
            "File to process contains {} file name part. Assuming the file is correct, skipping {}".format(
                filenamepart, file))
      else:
        filesNotContainingFilenamepart.append(file)
    return filesContainingFilenamepart, filesNotContainingFilenamepart

  def _filterOriginalFilesIfFileWithFilenamepartIsPresent(self, filesContainingTransformedFilenamepart=[],
      filesNotContainingTransformedFilenamepart=[], transformedFilenamePattern="", originalFilenamePattern=""):

    if (filesContainingTransformedFilenamepart == None):
      filesContainingTransformedFilenamepart = []
    if (filesNotContainingTransformedFilenamepart == None):
      filesNotContainingTransformedFilenamepart = []

    makeComparableString = "MAKE_COMPARABLE"
    # finding files with siblings
    candidatesForSiblings = set(
        map(lambda filename: filename.replace(transformedFilenamePattern, makeComparableString),
            set(filesContainingTransformedFilenamepart)))
    candidatesForOriginals = set(
        map(lambda filename: filename.replace(originalFilenamePattern, makeComparableString),
            set(filesNotContainingTransformedFilenamepart)))
    # find elements existing in both sets, i.e. having their processed counterpart already
    existingInBoth = candidatesForOriginals.intersection(candidatesForSiblings)
    existingInBothWithOriginalFilenamePattern = [file.replace(makeComparableString, originalFilenamePattern) for file in
                                                 existingInBoth]
    # remove all files with siblings
    # All files in their version of having filenamepart extended, not original
    processedFiles = list(
        map(lambda filename: filename.replace(makeComparableString, transformedFilenamePattern), existingInBoth))
    unprocessedFiles = list(
      set(filesNotContainingTransformedFilenamepart).difference(existingInBothWithOriginalFilenamePattern))
    return processedFiles, unprocessedFiles

  def _getFullFilenameWithoutExtension(self, fullpath):
    return os.path.splitext(fullpath)[0]

  def _getFileExtension(self, fullpath):
    return os.path.splitext(fullpath)[1]

  def _getFilenameWithoutExtension(self, fullpath):
    return os.path.splitext(os.path.basename(fullpath))[0]

  def _getFilenameWithExtension(self, fullpath):
    return os.path.basename(fullpath)

  def _getAllMediaFilesInBasepathExcludingChunkedFiles(self, basepath, filetypes={".mp4", ".wav"}):
    filelist = self._getAllMediaFilesInBasepath(basepath, filetypes)
    return [file for file in filelist if not ("mono_chunk_" in file)]

  def _getAllMediaFilesInBasepath(self, basepath, filetypes={".mp4", ".wav"}):
    filelist = []
    for dirpath, dirnames, filenames in os.walk(basepath):
      for filename in [f for f in filenames if self._getFileExtension(f) in filetypes]:
        filelist.append(os.path.join(dirpath, filename))
    self.logger.debug("Found {} {} files within basepath {}".format(len(filelist), filetypes, basepath))
    return filelist
