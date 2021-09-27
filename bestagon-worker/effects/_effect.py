class Effect:
  NAME = ''
  CONFIG = {}

  def __init__(self, pixels):
    self.pixels = pixels

  def run(self):
    pass

  @classmethod
  def register(self):
    return {
      'class': self,
      'name': self.NAME,
      'configs': self.CONFIG
    }
