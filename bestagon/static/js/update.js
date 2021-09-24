window.onload = () => {
  const updateButton = document.getElementById('updateButton');
  const spinner = document.getElementById('spinner');
  updateButton.disabled = true;

  updateButton.onclick = () => {
    if(updateButton.disabled) {
      return;
    }

    fetch('/api/update', {method: 'POST'})
      .then(response => response.json())
      .then(data => {
        if(data.success) {
          updateButton.disabled = true;
          spinner.classList.remove('is-hidden');

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
      updateButton.disabled = !data.update_available;
    });
};
