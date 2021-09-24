import threading
import subprocess


def update():
  threading.Thread(target=_update, daemon=True).start()


def _update():
  subprocess.call(['/bin/bash', '/srv/bestagon/install.sh'])
