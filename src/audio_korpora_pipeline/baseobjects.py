import logging


class LoggingObject(object):
  def __init__(self):
    self.logger = logging.getLogger(__name__)
