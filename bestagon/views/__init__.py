from .pages import pages

def register_views(app):
  app.register_blueprint(pages)
