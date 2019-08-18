import logging


class ConfiguredObject(object):
  def __init__(self, config, **kw):
    self.config = config


class LoggingObject(object):
  def __init__(self, **kw):
    self.logger = logging.getLogger(__name__)
