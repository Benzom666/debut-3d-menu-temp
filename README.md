# Début Bar & Restaurant website

A complete temporary public website for Début in downtown Barrie. The image-rich menu is one page of the site. The project is static HTML/CSS/JavaScript and can run on GitHub Pages or Sites.

## Preview

```sh
python3 -m http.server 8000 --directory dist
```

Open `http://localhost:8000/`. The temporary public address is `https://benzom666.github.io/debut-3d-menu-temp/`.

## Pages and live services

- `/` — restaurant landing page with venue photography, booking, menu, and events links
- `/restaurant/` — venue and experience
- `/menu/` — 92 menu items with AI-generated overhead imagery, a rotating featured plate, section navigation, item viewer, and print menu
- `/order/` — pickup request experience with spinning dishes, ingredient callouts for selected dishes, a saved cart, estimated HST, and Formspree submission
- `/events/` — October 2026 dates and weekly programming; expired dates hide automatically
- `/private-events/` — semi-private and full venue booking options with a direct inquiry
- `/book/` — reservation requests through Formspree, with direct phone and email options
- `/contact/` — address, directions, phone, email, and social links

Order online links open `/order/`. Pickup and reservation requests submit to the existing Formspree form. If a pickup request cannot be sent, the cart stays intact and an email fallback is shown. A request is not confirmed until the team replies, and no payment is taken on the site. Staff login still opens the original admin at `debutbar.ca/admin`.

The 92 food and drink visuals are AI-generated overhead images with transparent backgrounds. Full-resolution source PNGs are kept locally in `assets/generated-originals/` (excluded from Git); the committed, optimized WebP copies used throughout the site are in `dist/images/generated/`. The item viewer does not claim these are photographs of actual Début servings or offer AR. The print PDF QR opens the `/menu/` route on the temporary public domain. Actual item presentation may vary.

A [replacement reservation service](reservation-api/README.md) is under local development. It includes a private staff dashboard and D1-backed API, but the public site does not collect reservations through it until staff identities, notifications, and hosted storage are configured and verified.

## Edit and build

Update `build_full_site.py` for website copy, events, and the shared header/navigation, `dist/site.css` for the shared visual system, `menu-page.html` and `menu.json` for the menu, and `order-page.html`, `dist/order.css`, and `dist/order.js` for the pickup page. The menu and pickup templates contain a `SITE_HEADER` placeholder filled by the shared builder. Run:

```sh
python3 build.py
python3 build_full_site.py
python3 generate_qr.py
python3 export_pdf.py
```

Install dependencies from `requirements.txt` and Playwright Chromium for PDF export and browser checks. Verify with:

```sh
.venv/bin/python -m unittest discover -s tests -v
```

The menu was transcribed from `MENU DEBUT 2.pdf`. Some source drinks have no listed price, and promotional offers should be checked against the restaurant before long term publication. October 2026 event details came from the original [Début events page](https://debutbar.ca/events) on October 12, 2026. The dated October artwork and list retire on November 1 in Barrie time, leaving weekly programming and a link to current announcements. Private event formats came from the original [restaurant page](https://debutbar.ca/about).
