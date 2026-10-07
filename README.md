# Début 3D Menu

An interactive digital menu and a matching letter-size print PDF, based on `MENU DEBUT 2.pdf`.

## Open the menu

Open `dist/index.html` in a browser. Category links jump to each section. Cards use a subtle 3D tilt with a mouse; motion is removed when the system requests reduced motion.

The print file is `DEBUT-3D-Menu-Print.pdf`. The site also includes a download link for it.

## Edit and export

Edit `menu.json`, then run:

```sh
python3 build.py
python3 export_pdf.py
```

`build.py` creates `dist/menu-data.js`; `export_pdf.py` creates the root PDF and copies it into `dist/`.
PDF export requires Playwright and its Chromium browser (`pip install playwright` and `playwright install chromium`).

The source listed no prices for water, pop, juice, or bottled drinks, so these remain unpriced. Food names and numeric prices are preserved; descriptions have been lightly edited for spelling and clarity. Promotional offers are reproduced from the supplied menu and should be checked for current availability before public use.

The food hero image was generated for this project using the built-in image generation tool. Prompt: a photorealistic CGI composition of a double cheeseburger, butter chicken with naan, and creamy shrimp pasta on a transparent background, with warm gold-edged studio lighting and no text or logos.
