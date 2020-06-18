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

        pip install dist/audio_korpora_pipeline-0.10-py2.py3-none-any.whl

Getting Started
===============

This tool does not automatically download corpora from the internet, as download links will change over time anyway.
This means you have to get the data yourself and adjust the configuration according your filepaths.

The following is an example how to convert CommonVoice (Input) to M-AILABS and LJSpeech (Output)
Example command::

        audio_korpora_pipeline -c config.cfg --input_corpora="CommonVoice" --output_corpora="LJSpeech"

Other Example: Create one Fairseq-formatted output from three different datasets::

        audio_korpora_pipeline -c config.cfg --input_corpora="Archimob,ChJugendsprache,UntranscribedVideo" --output_corpora="FairseqWav2Vec"


Available Formats are:
#############################

.. _api:

Full list of available adapter are found within::

         audio_korpora_pipeline.py

InputAdapter
-------------

================== =====
InputAdapter       Compatible with
================== =====
CommonVoice        https://voice.mozilla.org/de/datasets (version de_538h_2019-12-10)
------------------ -----
UntranscribedVideo (any video collection without transcription with file-ending mp4)
------------------ -----
ChJugendsprache     https://clarin.phonetik.uni-muenchen.de/BASRepository/ Datensatz "CHJugendsprache"
------------------ -----
Archimob           https://www.spur.uzh.ch/en/departments/research/textgroup/ArchiMob.html (V2)
================== =====

OutputAdapter
-------------

=============== =====
OutputAdapter   Compatible with
=============== =====
M-AILABS        https://www.caito.de/2019/01/the-m-ailabs-speech-dataset/
--------------- -----
LJSpeech        https://data.keithito.com/data/speech/LJSpeech-1.1.tar.bz2
--------------- -----
FairseqWav2Vec  https://github.com/pytorch/fairseq/tree/v0.8.0
--------------- -----
OpenSeq2Seq     https://github.com/NVIDIA/OpenSeq2Seq/commit/61204b212cfe5c9ceda2be816b9052e9caf021a9
=============== =====









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

