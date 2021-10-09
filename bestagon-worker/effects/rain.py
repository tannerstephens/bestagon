import random
import time
import math

from led_map import led_map
from ._effect import Effect

class Rain(Effect):
  NAME = 'Rain'

  def __init__(self, pixels, r):
    super().__init__(pixels, r)

    self.drops = []
    self.top = -6
    self.bottom = 6
    self.top_width = 7

  def refresh_config(self):
    super().refresh_config()

    self.color = (
      self.config.get('Red').value,
      self.config.get('Green').value,
      self.config.get('Blue').value
    )

    self.sleep = self.config.get('Sleep').value

    self.chance, self.out_of = self.config.get('Chance').value.as_integer_ratio()

    self.decay_steps = self.config.get('Decay').value

    self.dr = math.ceil(self.color[0] // self.decay_steps + 0.5)
    self.dg = math.ceil(self.color[1] // self.decay_steps + 0.5)
    self.db = math.ceil(self.color[2] // self.decay_steps + 0.5)

  def setup_config(self):
    self.config.add('Red', 'number', int, 255)
    self.config.add('Green', 'number', int, 255)
    self.config.add('Blue', 'number', int, 255)
    self.config.add('Sleep', 'number', float, 0.05)
    self.config.add('Chance', 'number', float, 1/50)
    self.config.add('Decay', 'number', int, 7)
    return super().setup_config()

  def run(self):
    for i in range(len(self.pixels)):
      if self.pixels[i] != [0,0,0]:
        p = self.pixels[i]
        self.pixels[i] = (max(p[0] - self.dr,0),max(p[1] - self.dg,0),max(p[2] - self.db,0))

    for drop in self.drops:
      if random.getrandbits(1): # Left
        dq = -1

        if(drop[0] + dq, drop[1] + 1) not in led_map:
          dq = 0
      else: # Right
        dq = 0

        if(drop[0] + dq, drop[1] + 1) not in led_map:
          dq = -1

      drop[0] += dq
      drop[1] += 1

    self.drops = list(filter(lambda drop: drop[1] <= 6, self.drops))

    for i in range(self.top_width):
      if random.randint(0, self.out_of) < self.chance:
        self.drops.append([i,self.top])

    for drop in self.drops:
      t = tuple(drop)

      self.pixels[led_map[t]] = self.color

    self.pixels.show()
    time.sleep(self.sleep)
