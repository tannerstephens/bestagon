from flask import Flask

from .extensions import flask_redis
from .views import register_views

VERSION = '0.0.4'

def create_app(config='bestagon.config.Config'):
  app = Flask(__name__)
  app.config.from_object(config)

  register_extensions(app)
  register_views(app)

  return app


def register_extensions(app):
  flask_redis.init_app(app)
