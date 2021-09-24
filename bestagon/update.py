import threading
import subprocess


def update():
  threading.Thread(target=_update).start()


def _update():
  subprocess.call(['git', 'pull'], cwd='/srv/bestagon/')
  subprocess.call(['/bin/bash', '/srv/bestagon/install.sh'])
