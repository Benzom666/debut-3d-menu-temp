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

  const dateParts = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/Toronto', year: 'numeric', month: '2-digit', day: '2-digit',
  }).formatToParts(new Date());
  const parts = Object.fromEntries(dateParts.map(part => [part.type, part.value]));
  const localDate = `${parts.year}-${parts.month}-${parts.day}`;

  const datedEvents = [...document.querySelectorAll('.event-row[data-date]')];
  if (datedEvents.length) {
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
    let visible = 0;
    previews.forEach(preview => {
      preview.hidden = preview.dataset.date < localDate;
      if (!preview.hidden) visible++;
    });
    const empty = document.querySelector('.no-event-previews');
    if (empty) empty.hidden = visible > 0;
  }

  if (localDate >= '2026-11-01' && document.body.classList.contains('events-page')) {
    document.getElementById('events-title').innerHTML = 'Events at<br><em>Début.</em>';
    document.getElementById('events-intro').textContent = 'Live music, DJ nights and weekly gatherings in downtown Barrie. Check the latest schedule before visiting.';
    const cta = document.getElementById('events-hero-cta');
    cta.href = 'https://www.instagram.com/debutbar.ca/';
    cta.target = '_blank';
    cta.rel = 'noopener noreferrer';
    cta.innerHTML = 'Latest on Instagram <span>↗</span>';
    for (const selector of ['.event-poster', '#dates', '.event-banner']) {
      document.querySelector(selector).hidden = true;
    }
    document.querySelector('.weekly-latest').hidden = false;
  }
})();
