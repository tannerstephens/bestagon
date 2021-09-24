import threading
import subprocess

from .extensions import flask_redis

def update():
  threading.Thread(target=_update).start()

def check_for_update():
  subprocess.call(['git', 'remote', 'update'])
  git_status = subprocess.Popen(['git', 'status', '-uno'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = git_status.communicate()

  return 'Your branch is behind' in out.decode()

def _update():
  flask_redis.set('updating', 'true')
  subprocess.call(['git', 'pull'], cwd='/srv/bestagon/')
  subprocess.call(['/bin/bash', '/srv/bestagon/install.sh'])
