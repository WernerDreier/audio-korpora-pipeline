# -*- coding: utf-8 -*-

from enum import Enum


class ExistingInputAdapter(Enum):
  COMMON_VOICE = "CommonVoice"
  UNTRANSCRIBED_VIDEO = "UntranscribedVideo"
  CH_JUGENDSPRACHE = "ChJugendsprache"
  ARCHIMOB = "Archimob"
  SWISSTEXT2020_LOW_RESOURCE = "SwissText2020"


class ExistingOutputAdapter(Enum):
  MAILABS = "M-AILABS"
  LJ_SPEECH = "LJSpeech"
  FAIRSEQ_WAV2VEC = "FairseqWav2Vec"
  OPENSEQ2SEQ = "OpenSeq2Seq"
