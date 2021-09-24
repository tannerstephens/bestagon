import time
import board
import neopixel
import random
import math
import redis


redis_connection = redis.Redis(host='localhost', port=6379, db=0)

redis_connection.set('updating', 'false')

pixel_pin = board.D18
num_pixels = 127
sleep = 0.05
sparkle_color = (36,80,255)
flash_color = (128,128,128)
flash_steps = 1

sparkle_chance = 1
out_of = 500
decay_steps = 20

dr = math.ceil(sparkle_color[0] // decay_steps + 0.5)
dg = math.ceil(sparkle_color[1] // decay_steps + 0.5)
db = math.ceil(sparkle_color[2] // decay_steps + 0.5)


pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2,
  auto_write=False, pixel_order=neopixel.RGB)

pixels.fill((0,0,0))
pixels.show()

flash = [0 for _ in range(num_pixels)]

while True:
  state = redis_connection.get('state').decode()

  if state == 'sparkle':
    for i in range(num_pixels):
      if pixels[i] != [0,0,0]:
        if flash[i]:
          flash[i] -= 1

          if flash[i] == 0:
            pixels[i] = sparkle_color
        else:
          p = pixels[i]
          pixels[i] = (max(p[0] - dr,0),max(p[1] - dg,0),max(p[2] - db,0))

      if random.randint(0,out_of) < sparkle_chance:
        pixels[i] = flash_color
        flash[i] = flash_steps
    pixels.show()
    time.sleep(sleep)
  else:
    pixels.fill((0,0,0))
    pixels.show()
    time.sleep(0.5)
