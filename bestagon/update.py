import subprocess
import threading
from os import getcwd

from .extensions import flask_redis


def update():
  threading.Thread(target=_update).start()

def check_for_update():
  subprocess.call(['git', 'remote', 'update'])
  git_status = subprocess.Popen(['git', 'status', '-uno'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, _ = git_status.communicate()

  return 'Your branch is behind' in out.decode()

def _update():
  cwd = getcwd()

  flask_redis.set('updating', 'true')
  subprocess.call(['git', 'pull'], cwd='/srv/bestagon/')
  subprocess.call(['/bin/bash', f'{cwd}/install.sh'])
