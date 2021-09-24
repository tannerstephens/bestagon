from flask import Blueprint
from flask.templating import render_template
from ..update import update as update_app

pages = Blueprint('pages', __name__)


@pages.route('/')
def home():
  return render_template('home.html')


@pages.route('/update')
def update():
  return render_template('update.html')
