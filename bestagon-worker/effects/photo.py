from PIL import Image
from io import BytesIO
from base64 import b64decode
import time

from ._effect import Effect
from led_map import led_map
from math import sqrt


class Photo(Effect):
  NAME = 'Photo'

  def setup_config(self):
    self.config.add('Photo', 'image', str, '')
    self.config.add('Brightness', 'number', float, 0.5)

  def refresh_config(self):
    super().refresh_config()
    self.data_url = self.config.get('Photo').value
    self.brightness = self.config.get('Brightness').value

  def get_image(self):
    base64 = self.data_url.split(',')[1]

    return Image.open(BytesIO(b64decode(base64)))

  def run(self):
    image = self.get_image().resize((42,42))

    for (q,r) in led_map:
      x = (2 * (sqrt(3) * q + sqrt(3) / 2 * r))+21
      y = (2 * 1.5 * r)+18

      (red, green, blue) = image.getpixel((x,y))[:3]
      red = int(red * self.brightness)
      green = int(green * self.brightness)
      blue = int(blue * self.brightness)

      self.pixels[led_map[(q,r)]] = [red, green, blue]

    self.pixels.show()
    time.sleep(1)
