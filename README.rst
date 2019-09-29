audio-korpora-pipeline
======================

Tool transforms audio-korpora of given formats into desired output-formats.
Audio-Corpus could be M-AILABS, Apache CommonVoice or others.
Please consult the changelog to see which corpora are currently supported.


Installation
============

Like any wheel: pip install audio_korpora_pipeline-0.6_SNAPSHOT-py2.py3-none-any.whl

Getting Started
===============

This tool does not automatically download corpora from the internet, as download links will change over time anyway.
This means you have to get the data yourself and adjust the configuration according your filepaths.

The following is an example how to convert CommonVoice (Input) to M-AILABS and LJSpeech (Output)
Example command::

        audio_korpora_pipeline -c config.cfg --input_corpora="CommonVoice" --output_corpora="LJSpeech"


.. _api:

Available Adapter are found within::

         audio_korpora_pipeline.py



Configuration
=============

change configuration according your needs within config.cfg


Developing
==========

Describe how to setup a development environment
