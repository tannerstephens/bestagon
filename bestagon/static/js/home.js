window.onload = () => {
  const stateSelect = document.getElementById('stateSelect');

  const inSelect = value => {
    return (stateSelect.innerHTML.indexOf('value="' + value + '"') > -1)
  }

  fetch('/api/effects')
    .then(resp => resp.json())
    .then(data => {
      data.forEach(effect => {
        const opt = document.createElement('option');
        opt.value = effect;
        opt.innerHTML = effect;
        stateSelect.appendChild(opt);
      });

      fetch('/api/state')
        .then(response => response.json())
        .then(data => {
          if(inSelect(data.state)) {
            stateSelect.value = data.state;
          } else {
            stateSelect.selectedIndex = '0';
          }

        });
    });

  stateSelect.onchange = () => {
    fetch('/api/state', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({state: stateSelect.value})
    });
  };
}
