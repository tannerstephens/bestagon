from flask import Flask

from .views import register_views


def create_app():
  app = Flask(__name__)

  register_views(app)

  return app
