import time
import board
import neopixel
import redis
from glob import glob
from os import path

from importlib.util import spec_from_file_location, module_from_spec
from led_map import led_map

DIR = path.dirname(path.abspath(__file__))

class Worker:
  def __init__(self):
    self.pixel_pin = board.D18
    self.num_pixels = 127

    self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=0.2,
      auto_write=False, pixel_order=neopixel.RGB)

    self.redis_connection = redis.Redis(host='localhost', port=6379, db=0)
    self.redis_connection.set('updating', 'false')

    self.redis_connection.delete('effects')
    self.effects = {}

    self._load_effects()

  def _load_effects(self):
    for i, effect_path in enumerate(glob(f'{DIR}/effects/*.py')):
      spec = spec_from_file_location(f'plugin{i}', effect_path)
      effect = module_from_spec(spec)
      spec.loader.exec_module(effect)

      registered_effect = effect.register()

      clazz = registered_effect['class']
      name = registered_effect['name']

      self.effects[name] = clazz(self.pixels, led_map)
      self.redis_connection.rpush('effects', name)

  def run(self):
    last_state = None

    while True:
      state = self.redis_connection.get('state').decode()

      if last_state != state:
        self.pixels.fill((0,0,0))
        self.pixels.show()

      if state in self.effects:
        self.effects[state].run()
      else:
        self.pixels.fill((0,0,0))
        self.pixels.show()
        time.sleep(0.5)

      last_state = state

if __name__ == '__main__':
  worker = Worker()
  worker.run()
