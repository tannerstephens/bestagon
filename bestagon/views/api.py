from flask import Blueprint, request, jsonify

from ..extensions import flask_redis
from ..update import check_for_update, update

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/state', methods=['GET', 'POST'])
def state():
  if request.method == 'GET':
    current_state = flask_redis.get('state') or b''
    current_state = current_state.decode()
    return jsonify({
      'state': current_state
    })

  new_state = request.json.get('state')

  if new_state is None:
    return jsonify({
      'success': False,
      'message': 'Parameter "state" is required'
      }), 422

  flask_redis.set('state', new_state)

  return jsonify({
    'success': True
  })

@api.route('/update', methods=['GET', 'POST'])
def update_handler():
  if request.method == 'GET':
    return jsonify({
      'update_available': check_for_update()
    })

  if check_for_update():
    update()

    return jsonify({
      'success': True
    })

  return jsonify({
    'success': False
  })

@api.route('/updating')
def updating():
  updating = flask_redis.get('updating') or b'false'
  updating = updating.decode()

  return jsonify({
    'updating': updating == 'true'
  })

@api.route('/effects')
def get_effects():
  effects = flask_redis.lrange('effects', 0, -1)

  effects_decoded = [effect.decode() for effect in effects]

  return jsonify(effects_decoded)
