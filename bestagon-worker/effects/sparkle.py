import math
import random
import time

from ._effect import Effect


class Sparkle(Effect):
  NAME = 'Sparkle'

  def __init__(self, pixels, r):
    super().__init__(pixels, r)

    self.sleep = 0.05
    self.sparkle_color = (36,80,255)
    self.flash_color = (128,128,128)
    self.flash_steps = 1

    self.sparkle_chance = 1
    self.out_of = 500
    self.decay_steps = 20

    self.dr = math.ceil(self.sparkle_color[0] // self.decay_steps + 0.5)
    self.dg = math.ceil(self.sparkle_color[1] // self.decay_steps + 0.5)
    self.db = math.ceil(self.sparkle_color[2] // self.decay_steps + 0.5)

    self.flash = [0 for _ in range(len(self.pixels))]

  def run(self):
    for i in range(len(self.pixels)):
      if self.pixels[i] != [0,0,0]:
        if self.flash[i]:
          self.flash[i] -= 1

          if self.flash[i] == 0:
            self.pixels[i] = self.sparkle_color
        else:
          p = self.pixels[i]
          self.pixels[i] = (max(p[0] - self.dr,0),max(p[1] - self.dg,0),max(p[2] - self.db,0))

      if random.randint(0,self.out_of) < self.sparkle_chance:
        self.pixels[i] = self.flash_color
        self.flash[i] = self.flash_steps
    self.pixels.show()
    time.sleep(self.sleep)
