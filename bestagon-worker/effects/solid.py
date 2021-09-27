import time

from ._effect import Effect


class Solid(Effect):
  NAME = 'Solid'

  def __init__(self, pixels):
    super().__init__(pixels)
    self.color = (128,128,128)

  def run(self):
    self.pixels.fill(self.color)
    self.pixels.show()
    time.sleep(0.5)
