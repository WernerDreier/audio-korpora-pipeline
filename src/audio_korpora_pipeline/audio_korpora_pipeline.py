# -*- coding: utf-8 -*-

from enum import Enum


class ExistingInputAdapter(Enum):
  COMMON_VOICE = "CommonVoice"


class ExistingOutputAdapter(Enum):
  MAILABS = "M-AILABS"
  LJ_SPEECH = "LJSpeech"
