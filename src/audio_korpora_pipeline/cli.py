# -*- coding: utf-8 -*-

"""Console script for audio_korpora_pipeline."""

import argparse
import configparser
import logging
import os
import sys

from inputadapter.adapters import CommonVoiceAdapter
from outputadapter.adapters import LjSpeechAdapter, MailabsAdapter


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


def _createInputAdapters(config, inputs):
  adapters = []

  # parse input
  inputs = inputs.split(",")
  accepted_input_corpora = ['CommonVoice']
  # Create Adapters
  for input in inputs:
    if input not in accepted_input_corpora:
      raise ValueError('please enter valid input corpora type(s): {}'.format(accepted_input_corpora))
    if ("CommonVoice" == input):
      adapters.append(CommonVoiceAdapter(config))
  return adapters


def _createOutputAdapters(config, outputs):
  adapters = []
  # parse input
  outputs = outputs.split(",")
  accepted_output_corpora = ['LJSpeech', 'M-AILABS']
  # Create Adapters
  for output in outputs:
    if output not in accepted_output_corpora:
      raise ValueError('please enter valid output corpora type(s): {}'.format(accepted_output_corpora))
    if ("M-AILABS" == output):
      adapters.append(MailabsAdapter(config))
    if ("LJSpeech" == output):
      adapters.append(LjSpeechAdapter(config))
  return adapters


def _transformMetamodelsToOutputs(metamodels, output_adapters):
  for metamodel in metamodels:
    for output_adapter in output_adapters:
      output_adapter.fromMetamodel(metamodel)
  pass


def _transformInputsToMetamodel(input_adapters):
  metmodels = []
  for input_adapter in input_adapters:
    metmodels.append(input_adapter.toMetamodel())
  return metmodels


def main():
  """
    Console script for audio_korpora_pipeline.
    Implement here CLI args parsing

  """

  parser = argparse.ArgumentParser()
  parser.add_argument("-c", "--config", dest="config",
                      help="path to config file", required=True)
  parser.add_argument("-i", "--input_corpora", dest="input",
                      help="comma separated list of which corpora to transform", required=True)
  parser.add_argument("-o", "--output_corpora", dest="output",
                      help="comma separated list of which corpora to produce", required=True)

  args = parser.parse_args()
  config_path = args.config

  if not os.path.isfile(config_path):
    parser.print_help()

  config = __load_config(config_path)
  __config_logging(__load_config(config_path))

  # Creating Adapters
  input_adapters = _createInputAdapters(config, args.input)
  output_adapters = _createOutputAdapters(config, args.output)

  # Creating metamodels
  metamodels = _transformInputsToMetamodel(input_adapters)

  # Doing output work
  _transformMetamodelsToOutputs(metamodels, output_adapters)

  return 0


if __name__ == "__main__":
  sys.exit(main())  # pragma: no cover
