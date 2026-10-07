# Début 3D Menu

An interactive digital menu and a matching letter-size print PDF, based on `MENU DEBUT 2.pdf`.

## Open the menu

Open `dist/index.html` in a browser, or use the temporary public address at `https://benzom666.github.io/debut-3d-menu-temp/`. Category links jump to each section. Each menu entry has an illustrative 3D-style image that opens in a full-screen viewer; cards use a subtle 3D tilt with a mouse, and motion is removed when the system requests reduced motion.

The print file is `DEBUT-3D-Menu-Print.pdf`. The site also includes a download link for it.

## Edit and export

Edit `menu.json`, then run:

```sh
python3 build.py
python3 generate_qr.py
python3 integrate_images.py
python3 export_pdf.py
```

`build.py` creates `dist/menu-data.js`; `generate_qr.py` creates the scannable QR image; `integrate_images.py` converts generated art into WebP images; `export_pdf.py` creates the root PDF and copies it into `dist/`.
Install the listed Python dependencies with `pip install -r requirements.txt`; PDF export also requires Playwright Chromium (`playwright install chromium`).

The source listed no prices for water, pop, juice, or bottled drinks, so these remain unpriced. Food names and numeric prices are preserved; descriptions have been lightly edited for spelling and clarity. Promotional offers are reproduced from the supplied menu and should be checked for current availability before public use.

The food hero and item images were generated for this project with the built-in image generation tool. The shared item prompt calls for a photorealistic CGI render of the specific listed dish or drink, isolated on a transparent background, shown on a dark plate or suitable vessel under warm studio lighting, with no text or logos. These images are illustrative and may differ from actual plating.
