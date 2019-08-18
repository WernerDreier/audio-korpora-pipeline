import json
import logging


class LoggingObject(object):
  def __init__(self):
    self.logger = logging.getLogger(__name__)

  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__,
                      sort_keys=True, indent=4)
