from flask import Blueprint
from flask.templating import render_template
from ..update import update

pages = Blueprint('pages', __name__)


@pages.route('/')
def home():
  return render_template('home.html')


@pages.route('/update')
def update():
  update()

  return render_template('update.html')
