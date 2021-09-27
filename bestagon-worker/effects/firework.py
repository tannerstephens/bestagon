import math
import time
import random

from led_map import led_map
from ._effect import Effect

def random_color():
  return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

class Rip:
  def __init__(self, start, pixels, color):
    self.active = {start}
    self.seen = set()
    self.pixels = pixels
    self.color = color

  def step(self):
    self.seen.update(self.active)

    new_active = set()

    for p in self.active:
      for q, r in ((0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1)):
          check = (p[0] + q, p[1] + r)
          if check not in self.seen and check in led_map:
            new_active.add(check)


    self.active = new_active

    for p in self.active:
      self.pixels[led_map[p]] = self.color

  def is_empty(self):
    return len(self.active) == 0

class Firework(Effect):
  NAME = 'Firework'

  def __init__(self, pixels):
    super().__init__(pixels)
    self.pixels = pixels

    self.chance = 1
    self.out_of = 1000

    self.ripples = []

    self.dr = 85
    self.dg = 85
    self.db = 85

    self.sleep = 0.05

  def run(self):
    for i in range(len(self.pixels)):
      if self.pixels[i] != [0,0,0]:
        p = self.pixels[i]
        self.pixels[i] = (max(p[0] - self.dr,0),max(p[1] - self.dg,0),max(p[2] - self.db,0))

    for r in self.ripples:
      r.step()

    for point in led_map:
      if random.randint(0,self.out_of) < self.chance:
        color = random_color()
        self.ripples.append(Rip(point, self.pixels, color))
        self.pixels[led_map[point]] = color

    self.ripples = list(filter(lambda ripple: not ripple.is_empty(), self.ripples))

    self.pixels.show()
    time.sleep(self.sleep)
