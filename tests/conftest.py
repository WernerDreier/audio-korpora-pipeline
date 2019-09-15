#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

import pytest


def pytest_addoption(parser):
  parser.addoption("--input_corpora", action="store")
  parser.addoption("--output_corpora", action="store")


@pytest.fixture
def input_corpora(request):
  return request.config.getoption("--input_corpora")


@pytest.fixture
def output_corpora(request):
  return request.config.getoption("--output_corpora")
