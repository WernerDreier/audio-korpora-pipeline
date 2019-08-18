# -*- coding: utf-8 -*-

import configparser
import logging
import os


class Audiokorporapipeline:

  def __init__(self, config_path):
    """
        parse config, setup logging
    """

    self.__load_config(config_path)
    self.logger = logging.getLogger(__name__)

  def __load_config(self, config_path):
    """
        Parse config file

    """

    self.config = configparser.RawConfigParser()
    try:
      self.config.read_file(open(config_path))
    except IOError:
      raise RuntimeError("Can't read %s " % os.path.abspath(config_path))

  def fancy_function(self):
    """
      #TODO Implement

    """

    self.logger.debug("hello wolrd")

    pass
