from flask import Blueprint, request, jsonify

from ..extensions import flask_redis

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
