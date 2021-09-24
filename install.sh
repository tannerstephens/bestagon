python3 -m pip install pipenv
PIPENV_VENV_IN_PROJECT=1 pipenv install

cp bestagon-web.service /etc/systemd/system/bestagon-web.service
cp bestagon-worker.service /etc/systemd/system/bestagon-worker.service

systemctl daemon-reload
systemctl restart bestagon-web
systemctl restart bestagon-worker
