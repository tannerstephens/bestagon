from flask import Blueprint
from flask.templating import render_template

pages = Blueprint('pages', __name__)


@pages.route('/')
def home():
  return render_template('home.html')
