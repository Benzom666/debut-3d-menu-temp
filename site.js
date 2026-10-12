(() => {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.getElementById('global-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      nav.classList.toggle('is-open', open);
    });
    nav.addEventListener('click', event => {
      if (event.target.closest('a')) {
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-label', 'Open menu');
        nav.classList.remove('is-open');
      }
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && nav.classList.contains('is-open')) {
        toggle.click();
        toggle.focus();
      }
    });
  }

  const datedEvents = [...document.querySelectorAll('.event-row[data-date]')];
  if (datedEvents.length) {
    const today = new Date();
    const localDate = [today.getFullYear(), String(today.getMonth() + 1).padStart(2, '0'), String(today.getDate()).padStart(2, '0')].join('-');
    let visible = 0;
    datedEvents.forEach(event => {
      const past = event.dataset.date < localDate;
      event.hidden = past;
      if (!past) visible++;
    });
    const empty = document.querySelector('.no-events');
    if (empty) empty.hidden = visible > 0;
  }

  const previews = [...document.querySelectorAll('.event-preview[data-date]')];
  if (previews.length) {
    const today = new Date();
    const localDate = [today.getFullYear(), String(today.getMonth() + 1).padStart(2, '0'), String(today.getDate()).padStart(2, '0')].join('-');
    let visible = 0;
    previews.forEach(preview => {
      preview.hidden = preview.dataset.date < localDate;
      if (!preview.hidden) visible++;
    });
    const empty = document.querySelector('.no-event-previews');
    if (empty) empty.hidden = visible > 0;
  }
})();
