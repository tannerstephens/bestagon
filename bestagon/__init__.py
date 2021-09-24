from flask import Flask

from .views import register_views

VERSION = '0.0.2'

def create_app():
  app = Flask(__name__)

  register_views(app)

  return app
