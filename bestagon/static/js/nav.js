const setStatusPill = state => {
  const statusText = document.getElementById('statusText');
  const statusDot = document.getElementById('statusDot');

  if (!statusText) {
    return;
  }

  if (!state || state === 'none') {
    statusText.textContent = 'Idle';
    statusDot.classList.add('idle');
  } else {
    statusText.textContent = `${state} — running`;
    statusDot.classList.remove('idle');
  }
};

window.addEventListener('load', () => {
  fetch('/api/state')
    .then(resp => resp.json())
    .then(data => setStatusPill(data.state));
});
