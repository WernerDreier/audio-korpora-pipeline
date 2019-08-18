from baseobjects import LoggingObject, ConfiguredObject


class Adapter(LoggingObject, ConfiguredObject):
  def __init__(self, config):
    super(Adapter, self).__init__(config=config)

  def toMetamodel(self):
    raise NotImplementedError("Please use a subclass")


class ArchimobAdapter(Adapter):
  def toMetamodel(self):
    self.logger.debug("hello archomob input adapter")


class CommonVoiceAdapter(Adapter):
  def toMetamodel(self):
    self.logger.debug("hello CommonVoice Adapter")
