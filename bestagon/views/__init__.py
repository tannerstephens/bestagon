from .pages import pages
from .api import api

def register_views(app):
  app.register_blueprint(pages)
  app.register_blueprint(api)
