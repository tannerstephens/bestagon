const generate_config_inputs = effectName => {
  const configsDiv = document.getElementById('configs');
  configsDiv.innerHTML = '';

  fetch(`/api/configs?effect=${effectName}`)
    .then(resp => resp.json())
    .then(data => {
      data.forEach(config => {
        const configField = document.createElement('div');
        configField.classList.add('field')

        if(config.input_type === 'color') {

          configField.innerHTML = `
          <label class="label">${config.name}</label>
          <div class="control">
            <input data-jscolor="{format: 'rgb'}" id="${config.key}">
          </div>
          `
        } else {
          configField.innerHTML = `
            <label class="label">${config.name}</label>
            <div class="control">
              <input class="input" type="${config.input_type}" value="${config.value}" id="${config.key}">
            </div>
          `;
        }

        configsDiv.appendChild(configField);

        const input = configField.getElementsByTagName('input')[0]

        input.onchange = () => {
          fetch('/api/configs', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              config_key: input.id,
              value: input.value
            })
          });
        };
      });
    });
};

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
          generate_config_inputs(stateSelect.value);
        });
    });

  stateSelect.onchange = () => {
    fetch('/api/state', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({state: stateSelect.value})
    });

    generate_config_inputs(stateSelect.value);
  };
}
