import json
import logging


class LoggingObject(object):
  def __init__(self):
    self.logger = logging.getLogger(__name__)

  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__,
                      sort_keys=True, indent=4)

  """A mixin implementing a simple __repr__."""

  def __repr__(self):
    return "<{klass} {attrs}>".format(
        klass=self.__class__.__name__,
        attrs=" ".join("{}={!r}".format(k, v) for k, v in self.__dict__.items()),
    )

  def __hash__(self):
    return hash(self.__repr__())
