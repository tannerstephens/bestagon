import random
import time

from led_map import led_map
from ._effect import Effect


class Fire(Effect):
  NAME = 'Fire'

  def __init__(self, pixels, r):
    super().__init__(pixels, r)

    self.bottom = 6

    self.bottom_row = [p for p in led_map if p[1] == self.bottom]

    self.heat = {p: 0 for p in led_map}

  def setup_config(self):
    self.config.add('Color', 'color', tuple, (255, 60, 0))
    self.config.add('Sleep', 'number', float, 0.05)
    self.config.add('Chance', 'number', float, 1/3)
    self.config.add('Cooling', 'number', int, 25)

    return super().setup_config()

  def refresh_config(self):
    super().refresh_config()

    self.color = self.config.get('Color').value

    self.sleep = self.config.get('Sleep').value

    self.chance, self.out_of = self.config.get('Chance').value.as_integer_ratio()

    self.cooling = self.config.get('Cooling').value

  def heat_color(self, heat):
    color = self.color

    if heat < 128:
      t = heat / 128

      return (int(color[0] * t), int(color[1] * t), int(color[2] * t))

    t = (heat - 128) / 127

    return (
      int(color[0] + (255 - color[0]) * t),
      int(color[1] + (255 - color[1]) * t),
      int(color[2] + (255 - color[2]) * t),
    )

  def run(self):
    old_heat = self.heat
    new_heat = {}

    for p in self.bottom_row:
      heat = max(old_heat[p] - random.randint(0, self.cooling), 0)

      if random.randint(0, self.out_of) < self.chance:
        heat = min(heat + random.randint(160, 255), 255)

      new_heat[p] = heat

    for p in led_map:
      if p in new_heat:
        continue

      below = [q for q in ((p[0], p[1] + 1), (p[0] - 1, p[1] + 1)) if q in old_heat]

      avg = sum(old_heat[q] for q in below) // len(below) if below else 0

      new_heat[p] = max(avg - random.randint(0, self.cooling), 0)

    self.heat = new_heat

    for p, heat in self.heat.items():
      self.pixels[led_map[p]] = self.heat_color(heat)

    self.pixels.show()
    time.sleep(self.sleep)
