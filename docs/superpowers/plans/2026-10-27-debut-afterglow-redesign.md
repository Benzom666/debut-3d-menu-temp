# Début Afterglow Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild Début’s public website into the warm Afterglow visual system, remove arrow glyph controls, and preserve all content and workflows.

**Architecture:** Keep the existing Python-generated static site and its three CSS surfaces. Change source templates first, regenerate `dist/`, then apply semantic palette overrides to the full-site, menu, and pickup stylesheets. Browser tests verify rendered behavior rather than source strings.

**Tech Stack:** Python 3.12, static HTML/CSS/JavaScript, Playwright, unittest, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-10-27-debut-afterglow-redesign.md`

## Global Constraints

- Preserve existing routes, forms, menu data, supplied homepage media, and food-item imagery.
- Remove `↗`, `→`, `←`, `↑`, and `↓` from public controls.
- Keep desktop and 390px mobile layouts free of horizontal overflow.
- Maintain keyboard focus, reduced-motion behavior, and WCAG AA text contrast.

---

### Task 1: Replace glyph controls with explicit actions

**Files:**
- Modify: `build_full_site.py`
- Modify: `menu-page.html`
- Modify: `order-page.html`
- Modify: `dist/app.js`
- Modify: `dist/order.js`
- Test: `tests/test_site.py`

**Interfaces:**
- Consumes: existing page generator and public route templates.
- Produces: generated pages whose interactive labels use words rather than Unicode arrows.

- [ ] **Step 1: Run the failing rendered-DOM test**

Run: `python3.12 -m unittest discover -s tests -p 'test_site.py' -k arrow_glyphs`

Expected: FAIL on `index.html` because a rendered control contains `↗`.

- [ ] **Step 2: Replace controls in source templates**

Use explicit labels such as `Reserve`, `Previous`, `Next`, and `Back to top`; do not replace arrows with other Unicode symbols.

- [ ] **Step 3: Regenerate pages**

Run: `python3.12 build_full_site.py`

- [ ] **Step 4: Verify the arrow test passes**

Run: `python3.12 -m unittest discover -s tests -p 'test_site.py' -k arrow_glyphs`

Expected: PASS.

### Task 2: Apply the Afterglow visual system

**Files:**
- Modify: `dist/site.css`
- Modify: `dist/style.css`
- Modify: `dist/order.css`
- Test: `tests/test_site.py`

**Interfaces:**
- Consumes: current class names and semantic page structure.
- Produces: light paper canvases, oxblood actions, terracotta and sage feature fields, olive text, and deliberate dark media regions.

- [ ] **Step 1: Run the failing light-canvas test**

Run: `python3.12 -m unittest discover -s tests -p 'test_site.py' -k light_warm_canvas`

Expected: FAIL because the homepage body luminance is below `0.72`.

- [ ] **Step 2: Add semantic palette tokens and surface overrides**

Define canvas, paper, ink, muted, wine, clay, sage, brass, and on-dark roles. Use wine for primary actions and reserve brass for small accents and focus.

- [ ] **Step 3: Recompose the homepage and shared surfaces**

Keep the hero split, make content sections light, set the food feature to terracotta, events to sage, private-events media to oxblood, and footer to olive.

- [ ] **Step 4: Recompose menu and pickup surfaces**

Set both body canvases to ivory, preserve high-contrast navigation bands and media viewers, and make forms/drawers light.

- [ ] **Step 5: Verify the palette test passes**

Run: `python3.12 -m unittest discover -s tests -p 'test_site.py' -k light_warm_canvas`

Expected: PASS.

### Task 3: Validate and publish

**Files:**
- Modify if required: CSS and templates listed above.
- Create: `.impeccable/review/desktop.png`
- Create: `.impeccable/review/mobile.png`

**Interfaces:**
- Consumes: completed static build.
- Produces: verified source commit, published `main` commit, and live GitHub Pages deployment.

- [ ] **Step 1: Run the full site suite**

Run: `python3.12 -m unittest discover -s tests -p 'test_site.py'`

Expected: all tests PASS.

- [ ] **Step 2: Capture desktop and mobile screenshots**

Capture `1440×1000` and `390×844` full-page screenshots into `.impeccable/review/` and review them together.

- [ ] **Step 3: Run the Impeccable detector once**

Run: `node /Users/benzom/.codex/skills/impeccable/scripts/detect.mjs --json dist/index.html dist/site.css dist/style.css dist/order.css`

- [ ] **Step 4: Apply one correction batch and rerun tests**

Resolve mechanical detector findings and visible overflow/contrast issues, then rerun the full site suite.

- [ ] **Step 5: Commit and publish**

Commit source changes to `chore/debut-media-refresh`, fast-forward `site-source`, copy generated public files to the publishing worktree, and push `main`.

- [ ] **Step 6: Verify production**

Confirm the Pages build status is `built`, the built commit equals remote `main`, the live homepage contains no arrow glyphs, and the live body canvas is light.
