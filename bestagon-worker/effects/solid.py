import time

from ._effect import Effect

class Solid(Effect):
  NAME = 'Solid'

  def __init__(self, pixels, r):
    super().__init__(pixels, r)

  def setup_config(self):
    self.config.add('Color', 'color', tuple, (128,128,128))

    return super().setup_config()

  def run(self):
    self.color = self.config.get('Color').value

    self.pixels.fill(self.color)
    self.pixels.show()
    time.sleep(0.5)
