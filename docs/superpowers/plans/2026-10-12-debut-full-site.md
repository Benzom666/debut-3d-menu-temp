# Début Full Website Implementation Plan

**Goal:** Replace the temporary menu-only landing page with a complete public Début website while retaining the illustrated menu as one route.

**Architecture:** Generate static HTML pages into `dist/`; share CSS and JS; route bookings to direct phone and email contact, ordering to Clover, and staff login to the original admin while its data endpoint is secured.

**Tech Stack:** Python 3, HTML, CSS, JavaScript, Playwright, GitHub Pages, Sites static hosting.

**Spec:** `docs/superpowers/specs/2026-10-12-debut-full-site-design.md`

## Tasks

1. Write browser tests for the new page journey, outbound actions, and mobile navigation. Run them and confirm they fail on the menu-only site.
2. Generate homepage, events, restaurant, booking, contact, and menu routes from checked-in source. Share navigation, footer, page styling, and interaction code. Run the new tests to green.
3. Run all existing menu/image/print tests. Inspect desktop and mobile renders and repair concrete issues.
4. Update documentation, build artifacts, and QR destination as needed. Commit source changes, push the public GitHub Pages repository, and publish the existing Sites project.
