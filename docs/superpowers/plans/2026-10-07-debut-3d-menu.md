# Début 3D Menu Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a responsive 3D digital menu and matching print PDF from the supplied Début PDF.

**Architecture:** A JSON menu is the content source. A small build script validates it and emits a browser data file. A static HTML/CSS/JavaScript site renders the menu, and its print stylesheet produces the PDF.

**Tech Stack:** HTML, CSS, JavaScript, Python standard library, Playwright PDF export.

**Spec:** `docs/superpowers/specs/2026-10-07-debut-3d-menu-design.md`

## Global Constraints

- Preserve source item names and prices, with only obvious spelling corrections.
- Use the supplied charcoal, cream, and gold visual identity.
- Keep motion optional under `prefers-reduced-motion`.
- Do not invent prices for unpriced drinks.

---

### Task 1: Menu data

**Files:** `menu.json`, `tests/test_menu.py`, `build.py`, `dist/menu-data.js`

**Interfaces:** `menu.json` contains `sections` with `id`, `title`, and `items`; each item has `name`, optional `description`, and optional `price`. `build.py` emits `window.DEBUT_MENU`.

- [ ] Write tests for required sections, representative prices, unique item names, and beverage price omissions.
- [ ] Run tests and observe expected failure because data does not exist.
- [ ] Enter all menu content and write the validation/build script.
- [ ] Run tests and build; inspect item counts.

### Task 2: Digital menu

**Files:** `dist/index.html`, `dist/style.css`, `dist/app.js`, `dist/debut-food-hero.png`

**Interfaces:** The page reads `window.DEBUT_MENU`, renders section navigation and menu cards, and exposes keyboard-accessible links.

- [ ] Write browser assertions for section navigation, menu content, responsive viewport, and reduced motion.
- [ ] Observe expected failure before the site exists.
- [ ] Implement the responsive page and 3D styling.
- [ ] Run browser checks at desktop and mobile widths.

### Task 3: Print PDF

**Files:** `dist/style.css`, `DEBUT-3D-Menu-Print.pdf`

**Interfaces:** Browser print rendering of `dist/index.html` produces an upright letter-size PDF.

- [ ] Add print assertions for PDF page count and text presence.
- [ ] Observe expected failure before export.
- [ ] Add print stylesheet and export with Playwright.
- [ ] Render every PDF page and inspect for clipping and visual defects.

### Task 4: Delivery

**Files:** `.openai/hosting.json`, `README.md`

- [ ] Verify all local assets and scripts.
- [ ] Publish the static site privately through Sites if access is available.
- [ ] Record the live URL and local PDF/site paths in the handoff.
