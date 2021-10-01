from ._effect import Effect
from math import sin, pi
from time import sleep

class Wave(Effect):
  NAME = 'Wave'

  def __init__(self, pixels):
    super().__init__(pixels)

    self.color = (255,255,255)
    self.phase = 0

    self.rings = []

    self.sleep = 0.05

    l = 0

    for i in range(6,0,-1):
      self.rings.append((l,l+i*6-1))
      l += 6*i

    self.rings.append((126,126))

    self.phase_step = 2*pi / 7

  def run(self):
    self.phase += self.phase_step

    if self.phase >= 2*pi:
      self.phase -= 2*pi

    for i in range(len(self.rings)):
      start = self.rings[i][0]
      end = self.rings[i][1]

      s = (sin(self.phase + self.phase_step * i)+1)/2

      ring_color = (self.color[0] / s, self.color[1] / s, self.color[2] / s)

      for l in range(start,end+1):
        self.pixels[l] = ring_color

    self.pixels.show()
    sleep(self.sleep)
