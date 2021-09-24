import threading
import subprocess


def update():
  threading.Thread(target=_update).start()


def _update():
  subprocess.call(['/bin/bash', '/srv/bestagon/install.sh'])
