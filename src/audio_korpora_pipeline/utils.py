import os

from numpy import unicode


def winapi_path(dos_path, encoding=None):
  """
  Encods a path to work also on windows if necessary, otherwise assuming unix is able to work with long filepaths
  :param dos_path:
  :param encoding:
  :return:
  """
  given_path = dos_path
  if (is_windows_running() == True):
    if (not isinstance(dos_path, unicode) and encoding is not None):
      dos_path = dos_path.decode(encoding)
    path = os.path.abspath(dos_path)
    if path.startswith(u"\\\\"):
      return u"\\\\?\\UNC\\" + path[2:]
    return u"\\\\?\\" + path
  return given_path


def is_windows_running():
  if ("nt" == os.name):
    return True
  return False
