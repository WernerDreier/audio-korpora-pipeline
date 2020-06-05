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

  def _getFullFilenameWithoutExtension(self, fullpath):
    return os.path.splitext(fullpath)[0]

  def _getFileExtension(self, fullpath):
    return os.path.splitext(fullpath)[1]

  def _getFilenameWithoutExtension(self, fullpath):
    return os.path.splitext(os.path.basename(fullpath))[0]

  def _getFilenameWithExtension(self, fullpath):
    return os.path.basename(fullpath)

  def _getAllMediaFilesInBasepath(self, basepath, filetypes={".mp4", ".wav"}):
    file_list = []
    for dirpath, dirnames, filenames in os.walk(basepath):
      for filename in [f for f in filenames if self._getFileExtension(f) in filetypes]:
        file_list.append(os.path.join(dirpath, filename))
    self.logger.debug("Found {} {} files within basepath {}".format(len(file_list), filetypes, basepath))
    return file_list
