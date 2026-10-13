(() => {
  const heroVideo = document.querySelector('.home-hero video');
  if (heroVideo && matchMedia('(prefers-reduced-motion: reduce)').matches) {
    heroVideo.autoplay = false;
    heroVideo.pause();
  }
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
  const reserveForm = document.getElementById('reserve-form');
  if (reserveForm) {
    const fields = {
      name: document.getElementById('res-name'),
      email: document.getElementById('res-email'),
      phone: document.getElementById('res-phone'),
      date: document.getElementById('res-date'),
      time: document.getElementById('res-time'),
      guests: document.getElementById('res-guests'),
      message: document.getElementById('res-message'),
    };
    const status = document.getElementById('reserve-status');
    const mailtoBtn = document.getElementById('reserve-mailto');
    if (fields.date) fields.date.min = localDate;

    const showError = (input, id, message) => {
      const el = document.getElementById(id);
      if (!message) {
        if (el) el.hidden = true;
        if (input) input.removeAttribute('aria-invalid');
        return true;
      }
      if (el) {
        el.textContent = message;
        el.hidden = false;
      }
      if (input) input.setAttribute('aria-invalid', 'true');
      return false;
    };

    const isTuesday = value => {
      const day = new Date(`${value}T12:00:00Z`);
      return !Number.isNaN(day.getTime()) && day.toISOString().slice(0, 10) === value && day.getUTCDay() === 2;
    };

    const validate = () => {
      let firstInvalid = null;
      let ok = true;
      const mark = (input, id, msg) => {
        const valid = showError(input, id, msg);
        if (!valid && !firstInvalid) firstInvalid = input;
        if (!valid) ok = false;
      };

      const name = fields.name ? fields.name.value.trim() : '';
      mark(fields.name, 'err-res-name',
        name.length < 2 || name.length > 100 || /[<>]/.test(name) ? 'Name must be at least 2 characters' : '');

      const email = fields.email ? fields.email.value.trim() : '';
      mark(fields.email, 'err-res-email',
        email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) ? 'Invalid email address' : '');

      const phone = fields.phone ? fields.phone.value.trim() : '';
      const digits = phone.replace(/\D/g, '');
      mark(fields.phone, 'err-res-phone',
        phone.length > 30 || digits.length < 10 || /[<>]/.test(phone) ? 'Phone number must be at least 10 digits' : '');

      const date = fields.date ? fields.date.value : '';
      if (!date) mark(fields.date, 'err-res-date', 'Date is required');
      else if (date < localDate) mark(fields.date, 'err-res-date', 'Date cannot be in the past');
      else if (isTuesday(date)) mark(fields.date, 'err-res-date', 'Closed on Tuesdays');
      else mark(fields.date, 'err-res-date', '');

      const time = fields.time ? fields.time.value : '';
      mark(fields.time, 'err-res-time',
        !/^(?:[01]\d|2[0-3]):[0-5]\d$/.test(time) ? 'Time is required' : '');

      const guests = fields.guests ? Number(fields.guests.value) : 0;
      mark(fields.guests, 'err-res-guests',
        !Number.isInteger(guests) || guests < 1 || guests > 20 ? 'Select 1–20 guests' : '');

      return { ok, firstInvalid };
    };

    Object.values(fields).forEach(input => {
      if (!input) return;
      input.addEventListener('input', () => {
        input.removeAttribute('aria-invalid');
        const err = document.getElementById(`err-${input.id}`);
        if (err) err.hidden = true;
        if (status) status.hidden = true;
      });
    });
    if (fields.date) {
      fields.date.addEventListener('change', () => {
        const v = fields.date.value;
        if (v && v >= localDate && isTuesday(v)) showError(fields.date, 'err-res-date', 'Closed on Tuesdays');
      });
    }

    reserveForm.addEventListener('submit', event => {
      event.preventDefault();
      const { ok, firstInvalid } = validate();
      if (!ok) {
        if (status) {
          status.dataset.kind = 'error';
          status.textContent = 'Please fix the highlighted fields.';
          status.hidden = false;
        }
        if (firstInvalid) firstInvalid.focus();
        return;
      }
      const name = fields.name.value.trim();
      const email = fields.email.value.trim();
      const phone = fields.phone.value.trim();
      const date = fields.date.value;
      const time = fields.time.value;
      const guests = fields.guests.value;
      const message = fields.message ? fields.message.value.trim() : '';
      const body = [
        `Name: ${name}`,
        `Email: ${email}`,
        `Phone: ${phone}`,
        `Date: ${date}`,
        `Time: ${time}`,
        `Guests: ${guests}`,
        message ? `Requests: ${message}` : null,
      ].filter(Boolean).join('\n');
      const href = `mailto:info@debutbar.ca?subject=${encodeURIComponent(`Table reservation — ${name} — ${date} ${time}`)}&body=${encodeURIComponent(body)}`;
      if (mailtoBtn) {
        mailtoBtn.href = href;
        mailtoBtn.hidden = false;
      }
      const submitBtn = reserveForm.querySelector('button[type="submit"]');
      const originalLabel = submitBtn ? submitBtn.innerHTML : '';
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Sending…';
      }
      if (status) {
        status.dataset.kind = 'ok';
        status.textContent = 'Sending your request…';
        status.hidden = false;
      }
      fetch('https://formspree.io/f/mnpjboyk', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({
          name, email, phone, date, time, guests: Number(guests), message,
          _subject: `Table reservation — ${name} — ${date} ${time}`,
        }),
      }).then(async response => {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalLabel;
        }
        if (response.ok) {
          if (status) {
            status.dataset.kind = 'ok';
            status.textContent = `Thanks ${name} — your request for ${guests} on ${date} at ${time} was sent. The team will confirm by email or phone. Confirmed only after they reply.`;
            status.hidden = false;
          }
          reserveForm.reset();
          if (fields.guests) fields.guests.value = '2';
        } else {
          if (status) {
            status.dataset.kind = 'error';
            status.textContent = 'Could not send just now. Use “Email instead” to send your request, or call +1 942 883 3288.';
            status.hidden = false;
          }
        }
      }).catch(() => {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalLabel;
        }
        if (status) {
          status.dataset.kind = 'error';
          status.textContent = 'Network issue — use “Email instead” to send your request, or call +1 942 883 3288.';
          status.hidden = false;
        }
      });
    });
  }
})();
