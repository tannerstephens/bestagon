import time

class Solid:
  def __init__(self, pixels):
    self.pixels = pixels
    self.color = (128,128,128)

  def run(self):
    self.pixels.fill(self.color)
    self.pixels.show()
    time.sleep(0.5)

def register():
  return {
    'class': Solid,
    'name': 'Solid',
    'configs': {}
  }
