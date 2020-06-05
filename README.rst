audio-korpora-pipeline
======================

Tool transforms audio-korpora of given formats into desired output-formats.
Audio-Corpus could be M-AILABS, Apache CommonVoice or others.
Please consult the changelog to see which corpora are currently supported.


Installation
============
As the software-package is not yet available on pypi build the wheel yourself:

* Have Python 3.7.3 or higher installed
* Have pip installed
* Have wheel-support installed (if not use: pip install wheel)
* Build the wheel::

        python setup.py bdist_wheel

Then install like any wheel::

        pip install dist/audio_korpora_pipeline-0.9-py2.py3-none-any.whl

Getting Started
===============

This tool does not automatically download corpora from the internet, as download links will change over time anyway.
This means you have to get the data yourself and adjust the configuration according your filepaths.

The following is an example how to convert CommonVoice (Input) to M-AILABS and LJSpeech (Output)
Example command::

        audio_korpora_pipeline -c config.cfg --input_corpora="CommonVoice" --output_corpora="LJSpeech"

Another example Command is::

        audio_korpora_pipeline -c config.cfg --input_corpora="Archimob,ChJugendsprache,UntranscribedVideo" --output_corpora="FairseqWav2Vec"

.. _api:

Available Adapter are found within::

         audio_korpora_pipeline.py



Configuration
=============

change configuration according your needs within *config.cfg*


Tips for usage
==============
Running without interruptions
#############################
| As runtime of the pipeline is expected to be several hours (even though multithreading is used where possible), start the pipeline with a command, that detaches from your current user session. e.g.
| using:

**nohup** *command* **&**::

        nohup audio_korpora_pipeline -c ~/datasets/audio-korpora-pipeline-config.cfg --input_corpora='Archimob,UntranscribedVideo,ChJugendsprache' --output_corpora='FairseqWav2Vec' &

Watching progress
#################

| For watching progress either tail the configured log file (configuerd within *config.cfg*) or see if the process is still running::

Tail logs::

        tail -n 50 -f ~/repositories/audio-korpora-pipeline/log.log

Still running?::

        htop

