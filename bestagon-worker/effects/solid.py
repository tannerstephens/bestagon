import time

from ._effect import Effect

class Solid(Effect):
  NAME = 'Solid'

  def __init__(self, pixels, r):
    super().__init__(pixels, r)

  def setup_config(self):
    self.config.add_config('Red', 'number', int, 128)
    self.config.add_config('Green', 'number', int, 128)
    self.config.add_config('Blue', 'number', int, 128)

    return super().setup_config()

  def run(self):
    self.color = (
      self.config.get('Red').value,
      self.config.get('Green').value,
      self.config.get('Blue').value
    )

    self.pixels.fill(self.color)
    self.pixels.show()
    time.sleep(0.5)
