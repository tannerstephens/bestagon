import random
import time

from led_map import led_map

from ._effect import Effect


class Sand(Effect):
  NAME = 'Sand'

  def __init__(self, pixels, redis_conn):
    super().__init__(pixels, redis_conn)

    self.particles = set()

    self.top = -6
    self.bottom = 6
    self.top_width = 7

    self.fill = True

  def setup_config(self):
    self.config.add('Color', 'color', tuple, (128,128,128))

    self.config.add('Sleep', 'number', float, 0.05)
    self.config.add('Chance', 'number', float, 1/50)

    self.config.add('Threshold', 'number', float, 0.8)

    return super().setup_config()

  def refresh_config(self):
    super().refresh_config()

    self.color = self.config.get('Color').value

    self.sleep = self.config.get('Sleep').value

    self.chance, self.out_of = self.config.get('Chance').value.as_integer_ratio()

    self.threshold = self.config.get('Threshold').value

  def run(self):
    if len(self.particles) >= len(self.pixels) * self.threshold:
      self.fill = False

    elif len(self.particles) == 0:
      self.fill = True

    new_particles = set()

    for particle in self.particles:
      pos = []

      self.pixels[led_map[particle]] = self.color

      left = (particle[0] - 1, particle[1] + 1)
      right = (particle[0], particle[1] + 1)

      if (left in led_map or (not self.fill and (-6 <= left[0] <= 0))) and left not in new_particles and left not in self.particles:
        pos.append(left)

      if (right in led_map or (not self.fill and (-6 <= right[0] <= 0))) and right not in new_particles and right not in self.particles:
        pos.append(right)

      if len(pos) == 0:
        new_particles.add(particle)
        continue

      move = random.choice(pos)

      self.pixels[led_map[particle]] = (0,0,0)

      if move in led_map:
        self.pixels[led_map[move]] = self.color
        new_particles.add(move)

    self.particles = new_particles

    if self.fill:
      for i in range(self.top_width):
        if random.randint(0, self.out_of) < self.chance:
          self.particles.add((i,self.top))
          self.pixels[led_map[(i,self.top)]] = self.color

    self.pixels.show()
    time.sleep(self.sleep)
