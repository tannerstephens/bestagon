LOCK_HASH_FILE=".pipenv-lock-hash"
CURRENT_HASH=$(sha256sum Pipfile.lock | awk '{print $1}')

if [ ! -f "$LOCK_HASH_FILE" ] || [ "$(cat "$LOCK_HASH_FILE")" != "$CURRENT_HASH" ]; then
    PIPENV_VENV_IN_PROJECT=1 pipenv install
    echo "$CURRENT_HASH" > "$LOCK_HASH_FILE"
else
    echo "Pipfile.lock unchanged, skipping pipenv install"
fi

cp bestagon-web.service /etc/systemd/system/bestagon-web.service
cp bestagon-worker.service /etc/systemd/system/bestagon-worker.service

systemctl daemon-reload

systemctl enable bestagon-web
systemctl enable bestagon-worker

systemctl restart bestagon-worker
systemctl restart bestagon-web

redis-cli set updating false
