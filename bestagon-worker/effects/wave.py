from ._effect import Effect
from math import sin, pi
from time import sleep

class Wave(Effect):
  NAME = 'Wave'

  def __init__(self, pixels, r):
    super().__init__(pixels, r)

    self.phase = 0

    self.rings = []

    l = 0

    for i in range(6,0,-1):
      self.rings.append((l,l+i*6-1))
      l += 6*i

    self.rings.append((126,126))

  def setup_config(self):
    self.config.add('Color', 'color', tuple, (128,128,128))
    self.config.add('Sleep', 'number', float, 0.05)
    self.config.add('Phase Step', 'number', float, 2*pi / 40)
    self.config.add('Ring Step', 'number', float, 2*pi / 7)

    return super().setup_config()

  def refresh_config(self):
    self.color = self.config.get('Color').value

    self.sleep = self.config.get('Sleep').value

    self.phase_step = self.config.get('Phase Step').value
    self.ring_step = self.config.get('Ring Step').value

    return super().refresh_config()

  def run(self):
    self.phase += self.phase_step

    if self.phase >= 2*pi:
      self.phase -= 2*pi

    for i in range(len(self.rings)):
      start = self.rings[i][0]
      end = self.rings[i][1]

      s = (sin(self.phase + self.ring_step * i)+1)/2

      ring_color = (int(self.color[0] * s), int(self.color[1] * s), int(self.color[2] * s))

      for l in range(start,end+1):
        self.pixels[l] = ring_color

    self.pixels.show()
    sleep(self.sleep)
