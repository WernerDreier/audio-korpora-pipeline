# -*- coding: utf-8 -*-

"""Console script for audio_korpora_pipeline."""

import argparse
import configparser
import logging
import os
import sys

from inputadapter.adapters import ArchimobAdapter, CommonVoiceAdapter
from outputadapter.adapters import MailabsAdapter


def __load_config(config_path):
  """
      Parse config file

  """

  config = configparser.RawConfigParser()
  try:
    config.read_file(open(config_path))
  except IOError:
    raise RuntimeError("Can't read %s " % os.path.abspath(config_path))

  return config


def __config_logging(config):
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


def main():
  """
    Console script for audio_korpora_pipeline.
    Implement here CLI args parsing

  """

  parser = argparse.ArgumentParser()
  parser.add_argument("-c", "--config", dest="config",
                      help="path to config file", required=True)

  args = parser.parse_args()
  config_path = args.config

  if not os.path.isfile(config_path):
    parser.print_help()

  config = __load_config(config_path)

  __config_logging(__load_config(config_path))

  adapter = ArchimobAdapter(config)
  adapter.toMetamodel()

  commonVoiceAdapter = CommonVoiceAdapter(config)
  metamodel = commonVoiceAdapter.toMetamodel()

  mailabs_adapter = MailabsAdapter(config)
  mailabs_adapter.fromMetamodel(metamodel)

  return 0


if __name__ == "__main__":
  sys.exit(main())  # pragma: no cover