from ._config import Config

class Effect:
  NAME = ''

  def __init__(self, pixels, redis_conn):
    self.pixels = pixels
    self.redis_conn = redis_conn

    self.config_prefix = f'{self.NAME}_'

    self.config = Config(redis_conn, self.config_prefix)

    self.setup_config()

  def run(self):
    raise NotImplementedError

  def setup_config(self):
    self.redis_conn.set(f'{self.config_prefix}config_refresh', 'false')

  def _refresh_config(self):
    pass

  def refresh_config(self):
    # refresh = self.redis_conn.get(f'{self.config_prefix}config_refresh') or b''
    # if refresh.decode() == 'true':
    self._refresh_config()
    self.config.refresh()
    self.redis_conn.set(f'{self.config_prefix}config_refresh', 'false')
