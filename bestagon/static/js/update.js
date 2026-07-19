window.onload = () => {
  const updateButton = document.getElementById('updateButton');
  const spinner = document.getElementById('spinner');
  const badge = document.getElementById('updateBadge');
  const title = document.getElementById('updateTitle');
  const sub = document.getElementById('updateSub');
  updateButton.disabled = true;

  const showAvailable = () => {
    badge.textContent = 'Update available';
    badge.className = 'update-badge available';
    title.textContent = 'A new version is ready';
    sub.textContent = 'Installing restarts the device — it can take a few minutes.';
    updateButton.disabled = false;
  };

  const showCurrent = () => {
    badge.textContent = 'Up to date';
    badge.className = 'update-badge current';
    title.textContent = "You're on the latest version";
    sub.textContent = 'Check back later for the next update.';
    updateButton.disabled = true;
  };

  const showInstalling = () => {
    badge.textContent = 'Installing';
    badge.className = 'update-badge';
    title.textContent = 'Installing update';
    sub.textContent = 'The device will restart automatically once this finishes.';
    updateButton.disabled = true;
    updateButton.classList.add('is-hidden');
    spinner.classList.remove('is-hidden');
  };

  updateButton.onclick = () => {
    if(updateButton.disabled) {
      return;
    }

    fetch('/api/update', {method: 'POST'})
      .then(response => response.json())
      .then(data => {
        if(data.success) {
          showInstalling();

          const checkReload = () => {
            fetch('/api/updating')
              .then(response => response.json())
              .then(data => {
                if(!data.updating) {
                  window.location = '/';
                }
              });

            setTimeout(checkReload, 5000);
          }
          setTimeout(checkReload, 5000);
        }
      })
  };

  fetch('/api/update')
    .then(response => response.json())
    .then(data => {
      if(data.update_available) {
        showAvailable();
      } else {
        showCurrent();
      }
    });
};
