from json import loads, dumps

from redis import Redis


class Config:
  def __init__(self, redis_conn: Redis, config_prefix):
    self.redis_conn = redis_conn
    self.config_prefix = config_prefix

    self.configs = {}

  def add(self, name, input_type, transform_fn, default_value):
    new_config = ConfigValue(name, input_type, transform_fn, default_value)

    if not self.redis_conn.exists(f'{self.config_prefix}{name}'):
      self.redis_conn.set(f'{self.config_prefix}{name}', new_config.to_json())
    else:
      new_config.update(self.redis_conn.get(f'{self.config_prefix}{name}').decode())

    self.configs[name] = new_config

  def get(self, name):
    return self.configs[name]

  def refresh(self):
    for name, config in self.configs.items():
      config.update(self.redis_conn.get(f'{self.config_prefix}{name}').decode())

  def clean(self):
    existing_keys = {key.decode() for key in self.redis_conn.keys(f'{self.config_prefix}*')}
    real_keys = {f'{self.config_prefix}{key}' for key in self.configs.keys()}

    keys_to_remove = existing_keys.difference(real_keys)

    for key in keys_to_remove:
      self.redis_conn.delete(key)


class ConfigValue:
  def __init__(self, name, input_type, transform_fn, default_value):
    self.name = name
    self.input_type = input_type
    self.transform_fn = transform_fn
    self.value = default_value

  def to_json(self):
    return dumps({
      'name': self.name,
      'input_type': self.input_type,
      'value': self.value
    })

  def update(self, json):
    d = loads(json)

    self.value = self.transform_fn(d['value'])
