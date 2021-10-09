from flask import Blueprint, request, jsonify

from ..extensions import flask_redis
from ..update import check_for_update, update

from json import dumps, loads

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


@api.route('/configs', methods=['GET', 'POST'])
def get_configs():
  if request.method == 'GET':
    effect = request.args.get('effect')

    config_keys = flask_redis.keys(f'{effect}*')

    configs = []

    for config_key in config_keys:
      if b'config_refresh' not in config_key:
        config_json = flask_redis.get(config_key).decode()

        config = loads(config_json)
        config['key'] = config_key.decode()

        configs.append(config)

    return jsonify(configs)

  config_key = request.json.get('config_key')
  value = request.json.get('value')
  effect = config_key.split('_')[0]

  config_json = flask_redis.get(config_key).decode()
  config = loads(config_json)
  config['value'] = value

  flask_redis.set(config_key, dumps(config))
  flask_redis.set(f'{effect}_config_refresh', 'true')
  return jsonify({'success': True})
