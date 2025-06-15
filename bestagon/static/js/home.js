const readFile = file => {
  return new Promise((resolve, reject) => {
    var fr = new FileReader();
    fr.onload = () => {
      resolve(fr.result)
    };
    fr.onerror = reject;
    fr.readAsDataURL(file);
  });
}

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
            <input class="input" data-jscolor="{format: 'hex'}" id="${config.key}" value="rgb(${config.value[0]},${config.value[1]},${config.value[2]})">
          </div>
          `;
        } else if(config.input_type === 'image') {
          configField.innerHTML = `
          <figure class="image is-64x64">
            <img src="${config.value}">
          </figure>

          <div class="file">
            <label class="file-label">
              <input class="file-input" type="file" id="${config.key}" accept="image/*">
              <span class="file-cta">
                <span class="file-icon">
                  <i class="fa fa-upload"></i>
                </span>
                <span class="file-label">
                  Choose a file…
                </span>
              </span>
            </label>
          </div>
          `;
        } else if (config.input_type === 'checkbox') {
          const checked = config.value === '1' ? 'checked' : ''

          configField.innerHTML = `
            <label class="label">${config.name}</label>
            <div class="control">
              <input type="checkbox" id="${config.key}" ${checked}>
            </div>
          `
        } else {
          configField.innerHTML = `
            <label class="label">${config.name}</label>
            <div class="control">
              <input class="input" type="${config.input_type}" id="${config.key}" value="${config.value}" >
            </div>
          `;
        }

        configsDiv.appendChild(configField);

        const input = configField.getElementsByTagName('input')[0]

        input.onchange = () => {
          let value_promise = Promise.resolve(input.value);
          if(config.input_type === 'color') {
            const matches = input.jscolor.toRGBString().match(/rgb\((\d+),(\d+),(\d+)\)/).slice(1);
            value_promise = Promise.resolve(matches.map(v => parseInt(v)));
          } else if(config.input_type === 'image') {
            value_promise = readFile(input.files[0]).then(value => {
              configField.getElementsByTagName('img')[0].src = value;
              return value;
            });
          } else if(config.input_type === 'checkbox') {
            value_promise = Promise.resolve(input.checked ? '1' : '0')
          }

          value_promise.then(value => {
            fetch('/api/configs', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                config_key: input.id,
                value: value
              })
            });
          });
        };
      });
    }).then(() => jscolor.install());
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
