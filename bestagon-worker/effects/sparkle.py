import math
import random
import time

from ._effect import Effect


class Sparkle(Effect):
  NAME = 'Sparkle'

  def __init__(self, pixels, r):
    super().__init__(pixels, r)

    self.flash_color = (128,128,128)
    self.flash_steps = 1

    self.flash = [0 for _ in range(len(self.pixels))]

  def setup_config(self):
    self.config.add('Color', 'color', tuple, (128,128,128))

    self.config.add('Sleep', 'number', float, 0.05)
    self.config.add('Chance', 'number', float, 1/500)
    self.config.add('Decay', 'number', int, 7)

    return super().setup_config()

  def refresh_config(self):
    super().refresh_config()

    self.color = self.config.get('Color').value

    self.sleep = self.config.get('Sleep').value

    self.chance, self.out_of = self.config.get('Chance').value.as_integer_ratio()

    self.decay_steps = self.config.get('Decay').value

    self.dr = math.ceil(self.color[0] // self.decay_steps + 0.5)
    self.dg = math.ceil(self.color[1] // self.decay_steps + 0.5)
    self.db = math.ceil(self.color[2] // self.decay_steps + 0.5)

  def run(self):
    for i in range(len(self.pixels)):
      if self.pixels[i] != [0,0,0]:
        if self.flash[i]:
          self.flash[i] -= 1

          if self.flash[i] == 0:
            self.pixels[i] = self.color
        else:
          p = self.pixels[i]
          self.pixels[i] = (max(p[0] - self.dr,0),max(p[1] - self.dg,0),max(p[2] - self.db,0))

      if random.randint(0,self.out_of) < self.chance:
        self.pixels[i] = self.flash_color
        self.flash[i] = self.flash_steps
    self.pixels.show()
    time.sleep(self.sleep)
