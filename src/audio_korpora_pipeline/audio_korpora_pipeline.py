# -*- coding: utf-8 -*-

from enum import Enum


class ExistingInputAdapter(Enum):
  COMMON_VOICE = "CommonVoice"
  UNTRANSCRIBED_VIDEO = "UntranscribedVideo"
  CH_JUGENDSPRACHE = "ChJugendsprache"
  ARCHIMOB = "Archimob"


class ExistingOutputAdapter(Enum):
  MAILABS = "M-AILABS"
  LJ_SPEECH = "LJSpeech"
  FAIRSEQ_WAV2VEC = "FairseqWav2Vec"
