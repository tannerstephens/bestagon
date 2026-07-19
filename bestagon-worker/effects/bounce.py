import math
import random
import time

from led_map import led_map
from ._effect import Effect

SQRT3 = math.sqrt(3)

# Board geometry: led_map is a regular hexagon of axial cells with the
# given radius, centered on (0, 0). We simulate physics in continuous
# pixel space (pointy-top hex layout, y increasing downward, matching
# the "down" direction rain.py falls in) and snap to the nearest cell
# each frame for display.
_BOARD_RADIUS = max(max(abs(q), abs(r), abs(-q - r)) for q, r in led_map)

# Perpendicular distance from the board center to each edge, plus a little
# padding so balls visibly reach the outermost ring before bouncing back.
_APOTHEM = 1.5 * _BOARD_RADIUS + 0.75

# Outward unit normals of the hexagon's 6 straight edges, 60 degrees apart.
_EDGE_NORMALS = [
  (math.cos(math.radians(30 + 60 * i)), math.sin(math.radians(30 + 60 * i)))
  for i in range(6)
]


def axial_to_pixel(q, r):
  return SQRT3 * q + SQRT3 / 2 * r, 1.5 * r


def pixel_to_axial(x, y):
  r = y * 2 / 3
  q = x / SQRT3 - r / 2
  return q, r


def hex_round(q, r):
  s = -q - r
  rq, rr, rs = round(q), round(r), round(s)

  dq, dr, ds = abs(rq - q), abs(rr - r), abs(rs - s)

  if dq > dr and dq > ds:
    rq = -rr - rs
  elif dr > ds:
    rr = -rq - rs

  return int(rq), int(rr)


def nearest_cell(q, r):
  cell = hex_round(q, r)

  if cell in led_map:
    return cell

  # Padding lets the continuous position stray just outside the last ring
  # of real cells; fall back to whichever real cell is closest.
  return min(
    led_map,
    key=lambda c: abs(c[0] - q) + abs(c[1] - r) + abs((-c[0] - c[1]) - (-q - r)),
  )


class Ball:
  def __init__(self, pos, speed):
    self.x, self.y = axial_to_pixel(*pos)

    angle = random.uniform(0, 2 * math.pi)
    self.vx = math.cos(angle) * speed
    self.vy = math.sin(angle) * speed

  def step(self, gravity):
    # Leapfrog (half-kick, drift, half-kick) integration: splitting the
    # gravity kick around the drift is what makes this exactly
    # energy-conserving with the reflections below. Applying gravity as a
    # single full kick before (or after) the drift is only first-order
    # accurate and bleeds energy every step, which defeats the point of a
    # 100%-restitution bounce.
    vx, vy = self.vx, self.vy + 0.5 * gravity

    self.x += vx
    self.y += vy

    for nx, ny in _EDGE_NORMALS:
      overshoot = self.x * nx + self.y * ny - _APOTHEM

      if overshoot <= 0:
        continue

      # Push back onto the wall and mirror the velocity about its normal
      # (elastic collision, 100% restitution).
      self.x -= overshoot * nx
      self.y -= overshoot * ny

      v_along_normal = vx * nx + vy * ny
      if v_along_normal > 0:
        vx -= 2 * v_along_normal * nx
        vy -= 2 * v_along_normal * ny

    self.vx = vx
    self.vy = vy + 0.5 * gravity

  def cell(self):
    return nearest_cell(*pixel_to_axial(self.x, self.y))


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
    self.config.add('Gravity', 'number', float, 0.03)
    self.config.add('Speed', 'number', float, 0.6)

    return super().setup_config()

  def refresh_config(self):
    super().refresh_config()

    self.color = self.config.get('Color').value

    self.sleep = self.config.get('Sleep').value

    self.decay_steps = self.config.get('Decay').value

    self.dr = math.ceil(self.color[0] // self.decay_steps + 0.5)
    self.dg = math.ceil(self.color[1] // self.decay_steps + 0.5)
    self.db = math.ceil(self.color[2] // self.decay_steps + 0.5)

    self.gravity = self.config.get('Gravity').value
    self.speed = self.config.get('Speed').value

    self.count = self.config.get('Count').value

    while len(self.balls) < self.count:
      self.balls.append(Ball(random.choice(self.cells), self.speed))

    if len(self.balls) > self.count:
      self.balls = self.balls[:self.count]

  def run(self):
    for i in range(len(self.pixels)):
      if self.pixels[i] != [0,0,0]:
        p = self.pixels[i]
        self.pixels[i] = (max(p[0] - self.dr,0), max(p[1] - self.dg,0), max(p[2] - self.db,0))

    for ball in self.balls:
      ball.step(self.gravity)
      self.pixels[led_map[ball.cell()]] = self.color

    self.pixels.show()
    time.sleep(self.sleep)
