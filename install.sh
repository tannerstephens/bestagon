systemctl stop bestagon-worker

PIPENV_VENV_IN_PROJECT=1 pipenv install

cp bestagon-web.service /etc/systemd/system/bestagon-web.service
cp bestagon-worker.service /etc/systemd/system/bestagon-worker.service

systemctl daemon-reload

systemctl enable bestagon-web
systemctl enable bestagon-worker

systemctl start bestagon-worker
systemctl restart bestagon-web
