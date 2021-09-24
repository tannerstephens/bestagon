from flask import Flask

from .views import register_views

from .extensions import (
  flask_redis
)

VERSION = '0.0.3'

def create_app(config='bestagon.config.Config'):
  app = Flask(__name__)
  app.config.from_object(config)

  register_extensions(app)
  register_views(app)

  return app


def register_extensions(app):
  flask_redis.init_app(app)
