window.onload = () => {
  const updateButton = document.getElementById('updateButton');
  updateButton.disabled = true;

  updateButton.onclick = () => {
    if(updateButton.disabled) {
      return;
    }

    fetch('/api/update', {
      method: 'POST'
    });
  };

  fetch('/api/update')
    .then(response => response.json())
    .then(data => {
      updateButton.disabled = !data.update_available;
    });
};
