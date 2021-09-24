window.onload = () => {
  const stateSelect = document.getElementById('stateSelect');

  stateSelect.onchange = () => {
    fetch('/api/state', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({state: stateSelect.value})
    });
  };

  fetch('/api/state')
    .then(response => response.json())
    .then(data => {
      stateSelect.value = data.state;
    });
}
