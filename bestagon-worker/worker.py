import time
import board
import neopixel
import redis

from .effects.sparkle import Sparkle

pixel_pin = board.D18
num_pixels = 127

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2,
  auto_write=False, pixel_order=neopixel.RGB)

redis_connection = redis.Redis(host='localhost', port=6379, db=0)
redis_connection.set('updating', 'false')

pixels.fill((0,0,0))
pixels.show()

s = Sparkle(pixels)

while True:
  state = redis_connection.get('state').decode()

  if state == 'sparkle':
    s.run()
  else:
    pixels.fill((0,0,0))
    pixels.show()
    time.sleep(0.5)
