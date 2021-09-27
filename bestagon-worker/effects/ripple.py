import math
import time
import random

class Rip:
  def __init__(self, led_map, start):
    self.led_map = led_map
    self.active = {start}
    self.seen = set()

  def step(self):
    self.seen.update(self.active)

    new_active = set()

    for p in self.active:
      for q, r in ((0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1)):
          check = (p[0] + q, p[1] + r)
          if check not in self.seen and check in self.led_map:
            new_active.add(check)


    self.active = new_active

    for p in self.active:
      yield self.led_map[p]

  def is_empty(self):
    return len(self.active) == 0

class Ripple:
  def __init__(self, pixels, led_map):
    self.pixels = pixels
    self.led_map = led_map
    self.color = (255,255,255)

    self.chance = 1
    self.out_of = 1000

    self.ripples = []

    self.decay_steps = 3

    self.dr = math.ceil(self.color[0] // self.decay_steps + 0.5)
    self.dg = math.ceil(self.color[1] // self.decay_steps + 0.5)
    self.db = math.ceil(self.color[2] // self.decay_steps + 0.5)

    self.sleep = 0.05

  def run(self):
    for i in range(len(self.pixels)):
      if self.pixels[i] != [0,0,0]:
        p = self.pixels[i]
        self.pixels[i] = (max(p[0] - self.dr,0),max(p[1] - self.dg,0),max(p[2] - self.db,0))

    for r in self.ripples:
      for p in r.step():
        self.pixels[p] = self.color

    for point in self.led_map:
      if random.randint(0,self.out_of) < self.chance:
        self.ripples.append(Rip(self.led_map, point))
        self.pixels[self.led_map[point]] = self.color

    self.pixels.show()
    time.sleep(self.sleep)

def register():
  return {
    'class': Ripple,
    'name': 'Ripple',
    'configs': {}
  }
