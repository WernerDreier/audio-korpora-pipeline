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

  def filterAudioFilesContainingNamePattern(self, filelist, filenamepart, skipAlreadyProcessedFiles=True):
    processedFiles = []
    unprocessedFiles = []
    filesContainingFilenamepart, filesNotContainingFilenamepart = self._filterFilesNamedLikeTheFilenamepart(filelist,
                                                                                                            filenamepart)

    if (skipAlreadyProcessedFiles):
      self.logger.debug("Will remove original files from list too")
      processedFiles, unprocessedFiles = self._filterOriginalFilesIfFileWithFilenamepartIsPresent(
          filesContainingFilenamepart, filesNotContainingFilenamepart, filenamepart)
    else:
      processedFiles = filesContainingFilenamepart
      unprocessedFiles = filesNotContainingFilenamepart

    self.logger.debug(
        "Got {} files to process and {} already processed for filenamepart {} for given list of length {}".format(
            len(unprocessedFiles), len(processedFiles), filenamepart, len(filelist)))
    return processedFiles, unprocessedFiles

  def _filterFilesNamedLikeTheFilenamepart(self, filelist, filenamepart):
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

  def _filterOriginalFilesIfFileWithFilenamepartIsPresent(self, filesContainingFilenamepart=[],
      filesNotContainingFilenamepart=[], filenamepart=""):

    if (filesContainingFilenamepart == None):
      filesContainingFilenamepart = []
    if (filesNotContainingFilenamepart == None):
      filesNotContainingFilenamepart = []

    fileExtension = self._getFileExtension(filenamepart)
    # finding files with siblings
    candidatesForSiblings = set(
        map(lambda filename: filename.replace(filenamepart, fileExtension), set(filesContainingFilenamepart)))
    candidatesForOriginals = set(filesNotContainingFilenamepart)
    # find elements existing in both sets, i.e. having their processed counterpart already
    existingInBoth = candidatesForOriginals.intersection(candidatesForSiblings)
    # remove all files with siblings
    processedFiles = filesContainingFilenamepart
    processedFiles.extend(list(existingInBoth))
    unprocessedFiles = list(set(filesNotContainingFilenamepart).difference(set(processedFiles)))
    return processedFiles, unprocessedFiles

  def _getFullFilenameWithoutExtension(self, fullpath):
    return os.path.splitext(fullpath)[0]

  def _getFileExtension(self, fullpath):
    return os.path.splitext(fullpath)[1]

  def _getFilenameWithoutExtension(self, fullpath):
    return os.path.splitext(os.path.basename(fullpath))[0]

  def _getFilenameWithExtension(self, fullpath):
    return os.path.basename(fullpath)
