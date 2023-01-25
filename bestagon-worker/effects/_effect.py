from ._config import Config

class Effect:
  NAME = ''

  def __init__(self, pixels, redis_conn):
    self.pixels = pixels
    self.redis_conn = redis_conn

    self.config_prefix = f'{self.NAME}_'

    self.config = Config(redis_conn, self.config_prefix)

    self.setup_config()
    self.refresh_config()

  def run(self):
    raise NotImplementedError

  def setup_config(self):
    self.config.clean()

  def refresh_config(self):
    self.config.refresh()
