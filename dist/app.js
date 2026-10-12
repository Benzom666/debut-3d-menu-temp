(function () {
  const menu = window.DEBUT_MENU;
  if (!menu || !Array.isArray(menu.sections)) return;

  const links = document.getElementById('category-links');
  const sections = document.getElementById('sections');
  const viewer = document.getElementById('dish-viewer');
  const allEntries = [];
  let viewerIndex = 0;
  document.getElementById('menu-note').textContent = menu.note;

  const money = (value) => '$' + Number(value).toFixed(Number.isInteger(value) ? 0 : 1);
  const make = (tag, className, text) => {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  };

  menu.sections.forEach((section, sectionIndex) => {
    const link = make('a', 'category-link', section.title);
    link.href = '#' + section.id;
    links.append(link);

    const panel = make('section', 'menu-section');
    panel.id = section.id;
    panel.setAttribute('aria-labelledby', section.id + '-title');
    const head = make('div', 'section-head');
    const headingBlock = make('div', 'section-heading-block');
    headingBlock.append(make('p', 'section-number', String(sectionIndex + 1).padStart(2, '0') + ' / ' + String(menu.sections.length).padStart(2, '0')));
    headingBlock.append(make('h3', 'section-title', section.title));
    headingBlock.querySelector('h3').id = section.id + '-title';
    head.append(headingBlock, make('p', 'section-eyebrow', section.eyebrow));
    panel.append(head);

    const grid = make('div', 'items-grid');
    let lastGroup = null;
    section.items.forEach((item, itemIndex) => {
      if (item.group && item.group !== lastGroup) {
        grid.append(make('h4', 'item-group', item.group));
        lastGroup = item.group;
      }
      const article = make('article', 'menu-item');
      const imagePath = (window.DEBUT_ASSET_PREFIX || '') + 'images/' + section.id + '-' + String(itemIndex + 1).padStart(2, '0') + '.webp';
      const entryIndex = allEntries.push({ item, imagePath }) - 1;
      const visual = make('button', 'item-visual');
      visual.type = 'button';
      visual.setAttribute('aria-label', 'View 3D illustration of ' + item.name);
      const thumbnail = make('img', 'item-image');
      thumbnail.src = imagePath;
      thumbnail.alt = '';
      thumbnail.loading = 'lazy';
      thumbnail.decoding = 'async';
      thumbnail.width = 768;
      thumbnail.height = 768;
      visual.append(thumbnail, make('span', 'visual-action', 'VIEW 3D IMAGE ↗'));
      visual.addEventListener('click', () => openViewer(entryIndex));
      article.append(visual);
      const top = make('div', 'item-top');
      top.append(make('h4', 'item-name', item.name));
      const priceText = item.price !== undefined ? money(item.price) : (item.priceLabel || '');
      if (priceText) top.append(make('span', 'item-price', priceText));
      article.append(top);
      if (item.description) article.append(make('p', 'item-description', item.description));
      if (item.tags && item.tags.length) {
        const tags = make('div', 'item-tags');
        item.tags.forEach(tag => tags.append(make('span', 'item-tag', tag)));
        article.append(tags);
      }
      grid.append(article);
    });
    panel.append(grid);
    sections.append(panel);
  });

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        document.querySelectorAll('.category-link').forEach(link => {
          const active = link.getAttribute('href') === '#' + entry.target.id;
          if (active) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      }
    });
  }, { rootMargin: '-18% 0px -72% 0px' });
  document.querySelectorAll('.menu-section').forEach(section => observer.observe(section));

  function showViewerItem(index) {
    viewerIndex = (index + allEntries.length) % allEntries.length;
    const entry = allEntries[viewerIndex];
    document.getElementById('viewer-image').src = entry.imagePath;
    document.getElementById('viewer-image').alt = 'Illustrative 3D render of ' + entry.item.name;
    document.getElementById('viewer-name').textContent = entry.item.name + (entry.item.price !== undefined ? ' · ' + money(entry.item.price) : '');
    document.getElementById('viewer-description').textContent = entry.item.description || '';
    document.getElementById('viewer-count').textContent = String(viewerIndex + 1).padStart(2, '0') + ' / ' + String(allEntries.length).padStart(2, '0');
  }

  function openViewer(index) {
    showViewerItem(index);
    viewer.showModal();
    viewer.querySelector('.viewer-close').focus();
  }

  viewer.querySelector('.viewer-close').addEventListener('click', () => viewer.close());
  viewer.querySelector('.viewer-prev').addEventListener('click', () => showViewerItem(viewerIndex - 1));
  viewer.querySelector('.viewer-next').addEventListener('click', () => showViewerItem(viewerIndex + 1));
  viewer.addEventListener('click', event => { if (event.target === viewer) viewer.close(); });
  viewer.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') showViewerItem(viewerIndex - 1);
    if (event.key === 'ArrowRight') showViewerItem(viewerIndex + 1);
  });
  let touchStartX = 0;
  viewer.addEventListener('touchstart', event => { touchStartX = event.changedTouches[0].screenX; }, { passive: true });
  viewer.addEventListener('touchend', event => {
    const delta = event.changedTouches[0].screenX - touchStartX;
    if (Math.abs(delta) > 60) showViewerItem(viewerIndex + (delta < 0 ? 1 : -1));
  }, { passive: true });
  const viewerArt = viewer.querySelector('.viewer-art');
  viewerArt.addEventListener('touchmove', event => {
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const touch = event.touches[0];
    const rect = viewerArt.getBoundingClientRect();
    viewerArt.style.setProperty('--viewer-x', ((touch.clientY - rect.top) / rect.height - 0.5) * -12 + 'deg');
    viewerArt.style.setProperty('--viewer-y', ((touch.clientX - rect.left) / rect.width - 0.5) * 12 + 'deg');
  }, { passive: true });
  viewerArt.addEventListener('touchend', () => {
    viewerArt.style.removeProperty('--viewer-x');
    viewerArt.style.removeProperty('--viewer-y');
  }, { passive: true });
  if (matchMedia('(pointer: fine) and (prefers-reduced-motion: no-preference)').matches) {
    viewerArt.addEventListener('pointermove', event => {
      const rect = viewerArt.getBoundingClientRect();
      viewerArt.style.setProperty('--viewer-x', ((event.clientY - rect.top) / rect.height - 0.5) * -12 + 'deg');
      viewerArt.style.setProperty('--viewer-y', ((event.clientX - rect.left) / rect.width - 0.5) * 12 + 'deg');
    });
    viewerArt.addEventListener('pointerleave', () => {
      viewerArt.style.removeProperty('--viewer-x');
      viewerArt.style.removeProperty('--viewer-y');
    });
  }

  if (matchMedia('(pointer: fine) and (prefers-reduced-motion: no-preference)').matches) {
    document.querySelectorAll('.menu-item').forEach(card => {
      card.addEventListener('pointermove', event => {
        const rect = card.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width - 0.5;
        const y = (event.clientY - rect.top) / rect.height - 0.5;
        card.style.setProperty('--tilt-x', (-y * 3).toFixed(2) + 'deg');
        card.style.setProperty('--tilt-y', (x * 3).toFixed(2) + 'deg');
      });
      card.addEventListener('pointerleave', () => {
        card.style.removeProperty('--tilt-x');
        card.style.removeProperty('--tilt-y');
      });
    });
  }
})();
