# -*- coding: utf-8 -*-

from enum import Enum


class ExistingInputAdapter(Enum):
  COMMON_VOICE = 1
  ARCHIMOB = 2


class ExistingOutputAdapter(Enum):
  M_AILABS = 1
