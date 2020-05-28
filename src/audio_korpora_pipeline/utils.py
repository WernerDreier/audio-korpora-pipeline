import configparser
import logging
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


def load_config(config_path):
  """
      Parse config file

  """

  config = configparser.RawConfigParser()
  try:
    config.read_file(open(config_path))
  except IOError:
    raise RuntimeError("Can't read %s " % os.path.abspath(config_path))

  return config


def config_logging(config):
  """
      Setup logging config

  """

  logging.__defaultFormatter = logging.Formatter(u"%(message)s")
  log_file = config.get('logging', 'file')
  log_level_file = config.get('logging', 'file_level')
  log_level_stdout = config.get('logging', 'stdout_level')
  log = logging.getLogger()
  log.setLevel(logging.DEBUG)

  ch = logging.StreamHandler()
  ch.setLevel(log_level_stdout)

  fh = logging.FileHandler(log_file, encoding='utf-8')
  fh.setLevel(log_level_file)
  log.addHandler(ch)
  log.addHandler(fh)
  ch_fmt = logging.Formatter(config.get('logging', 'stdout_fmt'))
  fh_fmt = logging.Formatter(config.get('logging', 'file_fmt'))

  ch.setFormatter(ch_fmt)
  fh.setFormatter(fh_fmt)