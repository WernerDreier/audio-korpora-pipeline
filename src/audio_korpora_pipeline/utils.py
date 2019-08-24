import os

from numpy import unicode


def winapi_path(dos_path, encoding=None):
  if (not isinstance(dos_path, unicode) and encoding is not None):
    dos_path = dos_path.decode(encoding)
  path = os.path.abspath(dos_path)
  if path.startswith(u"\\\\"):
    return u"\\\\?\\UNC\\" + path[2:]
  return u"\\\\?\\" + path
