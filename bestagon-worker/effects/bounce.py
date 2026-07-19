import math
import random
import time

from led_map import led_map
from ._effect import Effect

DIRECTIONS = ((1,0),(1,-1),(0,-1),(-1,0),(-1,1),(0,1))


class Ball:
  def __init__(self, pos, direction):
    self.pos = pos
    self.direction = direction

  def step(self):
    for turn in (0, 1, -1, 2, -2, 3):
      d = (self.direction + turn) % 6
      dq, dr = DIRECTIONS[d]
      next_pos = (self.pos[0] + dq, self.pos[1] + dr)

      if next_pos in led_map:
        self.direction = d
        self.pos = next_pos
        return


class Bounce(Effect):
  NAME = 'Bounce'

  def __init__(self, pixels, r):
    self.cells = list(led_map.keys())

    self.balls = []

    super().__init__(pixels, r)

  def setup_config(self):
    self.config.add('Color', 'color', tuple, (128,128,128))
    self.config.add('Sleep', 'number', float, 0.05)
    self.config.add('Decay', 'number', int, 7)
    self.config.add('Count', 'number', int, 3)

    return super().setup_config()

  def refresh_config(self):
    super().refresh_config()

    self.color = self.config.get('Color').value

    self.sleep = self.config.get('Sleep').value

    self.decay_steps = self.config.get('Decay').value

    self.dr = math.ceil(self.color[0] // self.decay_steps + 0.5)
    self.dg = math.ceil(self.color[1] // self.decay_steps + 0.5)
    self.db = math.ceil(self.color[2] // self.decay_steps + 0.5)

    self.count = self.config.get('Count').value

    while len(self.balls) < self.count:
      self.balls.append(Ball(random.choice(self.cells), random.randrange(6)))

    if len(self.balls) > self.count:
      self.balls = self.balls[:self.count]

  def run(self):
    for i in range(len(self.pixels)):
      if self.pixels[i] != [0,0,0]:
        p = self.pixels[i]
        self.pixels[i] = (max(p[0] - self.dr,0), max(p[1] - self.dg,0), max(p[2] - self.db,0))

    for ball in self.balls:
      ball.step()
      self.pixels[led_map[ball.pos]] = self.color

    self.pixels.show()
    time.sleep(self.sleep)
