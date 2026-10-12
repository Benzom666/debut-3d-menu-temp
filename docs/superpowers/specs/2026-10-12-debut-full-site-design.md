# Début full website design

## Source audit

The existing public site has `/`, `/menu`, `/events`, `/about`, `/book`, `/contact`, and `/admin`. The homepage links to Clover online ordering. The October 2026 event calendar includes individual dated events plus weekly programming. The booking form posts to the existing site's private API; staff access is password protected and manages reservations. The venue is at 10 Dunlop St E, Barrie, ON L4M 1A3, with `info@debutbar.ca` and `+1 942 883 3288`. Public social accounts are Instagram and Facebook. Research source: https://debutbar.ca/ and its public routes, inspected October 12, 2026.

## Experience

Make a complete restaurant website with a cinematic editorial homepage, an illustrated menu page, a restaurant page grounded in actual venue photography, a dated events page, a reservations entry page, and a contact page. Use the real venue photography from the original website and a warm black, antique gold, and cream palette. Distinctive typography, generous spacing, asymmetrical compositions, and subtle motion should make the experience feel premium without obscuring practical information. Every page has clear routes to reserve, order, and contact.

## Architecture

Keep the temporary public site static on GitHub Pages and the existing Sites project. Generate real HTML routes under `dist/` from a small Python build script. Preserve the existing menu renderer and source data as its own `/menu/` page. Share one new stylesheet and script for navigation and reveal behavior. Use relative links that work under both the GitHub Pages repository path and the Sites domain.

For launch, the reservation page clearly hands off to the original live booking form, Clover remains the online order destination, and staff login goes to the original admin. This avoids inventing credentials or silently losing reservation submissions while the owner decides whether to migrate the backend. No external data is submitted by the new static site.

## Content and interaction

Homepage: venue promise, real interior imagery, menu preview, restaurant story, upcoming event preview, and a final reservation call to action. Events: October 2026 dates verified from the original site, ordered by date with past events visually marked; weekly programming described separately. Restaurant: experience, food, drinks, and private events using verified source claims. Contact: working mail, phone, maps, and social links. Booking: clear expectations and a link to the live reservation form. Mobile: compact navigation, accessible toggle, no horizontal overflow. Respect reduced motion and focus states.

## Verification and publication

Browser tests cover route content, navigation, mobile overflow, and outbound actions. Existing menu and PDF tests continue to pass. Inspect desktop and mobile screenshots. Commit the source, push the GitHub Pages deployment repository, then publish the corresponding Sites version. Keep localhost serving the updated `dist/` folder.

## Known boundary

The existing 92 menu visuals are illustrations, not rotatable geometry or AR models. Do not claim they provide 360-degree rotation or AR. Full item-by-item 3D capture or modeling remains a separate production requirement.
