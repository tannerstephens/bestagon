import random
import time
import math

class Rain:
  def __init__(self, pixels, led_map):
    self.pixels = pixels
    self.led_map = led_map
    self.color = (255,255,255)
    self.sleep = 0.05

    self.drops = []
    self.chance = 1
    self.out_of = 50

    self.top = -6
    self.bottom = 6

    self.top_width = 7

    self.decay_steps = 7

    self.dr = math.ceil(self.color[0] // self.decay_steps + 0.5)
    self.dg = math.ceil(self.color[1] // self.decay_steps + 0.5)
    self.db = math.ceil(self.color[2] // self.decay_steps + 0.5)

  def run(self):
    for i in range(len(self.pixels)):
      if self.pixels[i] != [0,0,0]:
        p = self.pixels[i]
        self.pixels[i] = (max(p[0] - self.dr,0),max(p[1] - self.dg,0),max(p[2] - self.db,0))

    for drop in self.drops:
      if random.getrandbits(1): # Left
        dq = -1

        if(drop[0] + dq, drop[1] + 1) not in self.led_map:
          dq = 0
      else: # Right
        dq = 0

        if(drop[0] + dq, drop[1] + 1) not in self.led_map:
          dq = -1

      drop[0] += dq
      drop[1] += 1

    self.drops = list(filter(lambda drop: drop[1] <= 6, self.drops))

    for i in range(self.top_width):
      if random.randint(0, self.out_of) < self.chance:
        self.drops.append([i,self.top])

    for drop in self.drops:
      t = tuple(drop)

      self.pixels[self.led_map[t]] = self.color

    self.pixels.show()
    time.sleep(self.sleep)

def register():
  return {
    'class': Rain,
    'name': 'Rain',
    'configs': {}
  }
