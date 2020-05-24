# -*- coding: utf-8 -*-

"""Console script for audio_korpora_pipeline."""

import argparse
import os
import sys

from audio_korpora_pipeline.audio_korpora_pipeline import ExistingOutputAdapter, ExistingInputAdapter
from audio_korpora_pipeline.inputadapter.adapters import CommonVoiceAdapter, UntranscribedVideoAdapter, \
  ChJugendspracheAdapter
from audio_korpora_pipeline.outputadapter.adapters import LjSpeechAdapter, MailabsAdapter, FairseqWav2VecAdapter
from audio_korpora_pipeline.utils import load_config, config_logging


def _createInputAdapters(config, inputs):
  adapters = []

  # parse input
  inputs = inputs.split(",")
  accepted_input_corpora = [l.value for l in ExistingInputAdapter]
  # Create Adapters
  for input in inputs:
    if input not in accepted_input_corpora:
      raise ValueError('please enter valid input corpora type(s): {}'.format(accepted_input_corpora))
    if (ExistingInputAdapter.COMMON_VOICE.value == input):
      adapters.append(CommonVoiceAdapter(config))
    if (ExistingInputAdapter.UNTRANSCRIBED_VIDEO.value == input):
      adapters.append(UntranscribedVideoAdapter(config))
    if (ExistingInputAdapter.CH_JUGENDSPRACHE.value == input):
      adapters.append(ChJugendspracheAdapter(config))
  return adapters


def _createOutputAdapters(config, outputs):
  adapters = []
  # parse input
  outputs = outputs.split(",")
  accepted_output_corpora = [l.value for l in ExistingOutputAdapter]
  print(accepted_output_corpora)
  # Create Adapters
  for output in outputs:
    if output not in accepted_output_corpora:
      raise ValueError('please enter valid output corpora type(s): {}'.format(accepted_output_corpora))
    if (ExistingOutputAdapter.MAILABS.value == output):
      adapters.append(MailabsAdapter(config))
    if (ExistingOutputAdapter.LJ_SPEECH.value == output):
      adapters.append(LjSpeechAdapter(config))
    if (ExistingOutputAdapter.FAIRSEQ_WAV2VEC.value == output):
      adapters.append(FairseqWav2VecAdapter(config))
  return adapters


def _transformMetamodelsToOutputs(metamodels, output_adapters):
  for index, output_adapter in enumerate(output_adapters):
    if (index == 0):
      output_adapter.cleanOutputFolder()
    for metamodel in metamodels:
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

  config = load_config(config_path)
  config_logging(load_config(config_path))

  # Creating Adapters
  input_adapters = _createInputAdapters(config, args.input)
  output_adapters = _createOutputAdapters(config, args.output)

  print("Started with {} input corpora to transform".format(len(input_adapters)))
  print("Started with {} output corpora as target format".format(len(output_adapters)))

  # Creating metamodels
  metamodels = _transformInputsToMetamodel(input_adapters)

  # Doing output work
  _transformMetamodelsToOutputs(metamodels, output_adapters)

  return 0


if __name__ == "__main__":
  sys.exit(main())  # pragma: no cover
