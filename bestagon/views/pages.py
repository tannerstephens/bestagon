from flask import Blueprint
from flask.templating import render_template

pages = Blueprint('pages', __name__)


@pages.route('/')
def home():
  return render_template('home.html', active_page='control')


@pages.route('/update')
def update():
  return render_template('update.html', active_page='update')
