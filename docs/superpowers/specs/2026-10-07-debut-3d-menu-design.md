# Début 3D Menu Design

## Purpose

Create a responsive interactive menu and a matching print-ready PDF from the supplied four-page Début menu. The two outputs share one source of menu content and the existing charcoal, cream, and gold palette.

## Content

Keep every listed food item and price. Correct obvious spelling errors in descriptions. Keep beverage entries without a printed price unpriced rather than inventing prices. Include add-ons, drinks, deals, and the tax note. Lay all pages upright; the source contains inverted panels for print folding.

## Digital experience

A single responsive page opens directly on the food menu. A dimensional food composition anchors the cover area, with layered section cards, subtle pointer tilt, and section navigation. All text stays in normal HTML for readability, selection, and screen readers. Motion respects reduced-motion settings. The menu works with mouse, keyboard, and touch.

## Print experience

Export a letter-size portrait PDF from the same content. Use a branded cover and compact, upright category pages. The dimensional food artwork is static in print. Prevent clipped items and orphaned headings.

## Technical design

`menu.json` is the source of truth. `build.py` validates it and creates the browser's `menu-data.js`. The web files live in `dist/`; a browser print stylesheet produces the PDF. Tests check content integrity and browser interactions. The deliverables are the `dist/` site and `DEBUT-3D-Menu-Print.pdf`.
