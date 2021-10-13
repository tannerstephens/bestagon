import time
import random

from ._effect import Effect
from led_map import led_map

class Bolt:
  def __init__(self, bottom, start):
    self.bottom = bottom

    self.trail = [start]

    self.generate()

  def generate(self):
    while self.trail[-1][1] < self.bottom:
      e = self.trail[-1]

      if random.getrandbits(1): # Left
        dq = -1
        if(e[0] + dq, e[1] + 1) not in led_map:
          dq = 0
      else: # Right
        dq = 0
        if(e[0] + dq, e[1] + 1) not in led_map:
          dq = -1

      self.trail.append((e[0] + dq, e[1] + 1))

  def regenerate(self, start):
    self.trail = [start]

    self.generate()

  def flash(self, color, pixels):
    for e in self.trail:
      pixels[led_map[e]] = color


class Lightning(Effect):
  NAME = 'Lightning'

  def __init__(self, pixels, r):
    super().__init__(pixels, r)

    self.bolts = []
    self.top = -6
    self.bottom = 6
    self.top_width = 7

    self.bolt = None
    self.bolt_active = False
    self.bolt_life = 0

  def setup_config(self):
    self.config.add('Red', 'number', int, 128)
    self.config.add('Green', 'number', int, 128)
    self.config.add('Blue', 'number', int, 128)
    self.config.add('Sleep', 'number', float, 0.03)
    self.config.add('Chance', 'number', float, 1/50)
    self.config.add('Life', 'number', int, 2)

    return super().setup_config()

  def refresh_config(self):
    super().refresh_config()

    self.color = (
      self.config.get('Red').value,
      self.config.get('Green').value,
      self.config.get('Blue').value
    )

    self.sleep = self.config.get('Sleep').value

    self.chance, self.out_of = self.config.get('Chance').value.as_integer_ratio()

    self.life = self.config.get('Life').value

  def run(self):
    self.pixels.fill((0,0,0))
    if self.bolt is None:
      self.bolt = Bolt(self.bottom, (random.randint(0, self.top_width-1), self.top))
      self.bolt_life = self.life

    self.bolt_active = self.bolt_active or random.randint(0, self.out_of) < self.chance

    if self.bolt_active:
      self.bolt_life -= 1
      self.bolt.flash(self.color, self.pixels)

    if self.bolt_life <= 0:
      self.bolt = None

    self.pixels.show()
    time.sleep(self.sleep)
