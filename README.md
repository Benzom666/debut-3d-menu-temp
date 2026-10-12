# Début Bar & Restaurant website

A complete temporary public website for Début in downtown Barrie. The illustrated menu is one page of the site. The project is static HTML/CSS/JavaScript and can run on GitHub Pages or Sites.

## Preview

```sh
python3 -m http.server 8000 --directory dist
```

Open `http://localhost:8000/`. The temporary public address is `https://benzom666.github.io/debut-3d-menu-temp/`.

## Pages and live services

- `/` — home
- `/restaurant/` — venue and experience
- `/menu/` — 92 illustrated menu items, section navigation, item viewer, and print menu
- `/events/` — October 2026 dates and weekly programming; expired dates hide automatically
- `/book/` — direct phone and email reservation requests
- `/contact/` — address, directions, phone, email, and social links

Ordering goes to the verified Clover ordering URL. Staff login still opens the original admin at `debutbar.ca/admin`. The booking page uses phone and email because the original reservation data endpoint needs server-side access control before directing new guests to that form. No reservation data is collected by this static site.

The food and drink visuals are illustrations, not rotatable 3D assets or augmented reality models. The print PDF QR opens the `/menu/` route on the temporary public domain. Actual item presentation may vary.

A [replacement reservation service](reservation-api/README.md) is under local development. It includes a private staff dashboard and D1-backed API, but the public site does not collect reservations through it until staff identities, notifications, and hosted storage are configured and verified.

## Edit and build

Update `build_full_site.py` for website copy and events, `dist/site.css` for the shared visual system, and `menu-page.html` and `menu.json` for the menu. Run:

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

The menu was transcribed from `MENU DEBUT 2.pdf`. Some source drinks have no listed price, and promotional offers should be checked against the restaurant before long term publication. October 2026 event details came from the original [Début events page](https://debutbar.ca/events) on October 12, 2026.
