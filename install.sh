log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

LOCK_HASH_FILE=".pipenv-lock-hash"
CURRENT_HASH=$(sha256sum Pipfile.lock | awk '{print $1}')

if [ ! -f "$LOCK_HASH_FILE" ] || [ "$(cat "$LOCK_HASH_FILE")" != "$CURRENT_HASH" ]; then
    log "Pipfile.lock changed, running pipenv install"
    PIPENV_VENV_IN_PROJECT=1 pipenv install
    echo "$CURRENT_HASH" > "$LOCK_HASH_FILE"
    log "pipenv install complete"
else
    log "Pipfile.lock unchanged, skipping pipenv install"
fi

log "Installing systemd unit files"
cp bestagon-web.service /etc/systemd/system/bestagon-web.service
cp bestagon-worker.service /etc/systemd/system/bestagon-worker.service

log "Reloading systemd daemon"
systemctl daemon-reload

systemctl enable bestagon-web
systemctl enable bestagon-worker

log "Restarting bestagon-worker"
systemctl restart bestagon-worker

log "Scheduling updating flag reset"
systemd-run --quiet --on-active=5 redis-cli set updating false

log "Restarting bestagon-web"
systemctl restart bestagon-web

log "Install complete"
