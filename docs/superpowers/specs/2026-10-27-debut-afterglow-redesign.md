# Début Afterglow Redesign

## Intent

Replace the near-black visual world with a warm, editorial restaurant experience that carries visitors from dinner into nightlife. Preserve every factual claim, route, form, menu item, and supplied media asset. Remove Unicode arrows from the interface and make every action self-explanatory.

## Direction: The Afterglow Line

The site behaves like a beautifully printed dining-car itinerary: warm paper, oxblood route bands, olive ink, terracotta dining surfaces, and restrained brass accents. The reference is structural rather than decorative—clear stages, decisive typography, deliberate borders, and a visible transition from daylight warmth to evening colour. There are no train illustrations, novelty tickets, faux stamps, or literal railway copy.

### First viewport

The homepage opens as a split editorial composition. The vertical supplied reel owns the right side; the left side uses warm ivory, oversized olive type, and one oxblood action block. The composition must communicate restaurant, nightlife, Barrie, and the booking action within the first viewport. Mobile becomes a full-bleed reel with a warm paper text panel anchored beneath it, not a dark overlay covering the subject.

### Visitor path

1. **Arrival:** the hero presents the venue and booking/menu actions.
2. **The room:** the supplied booth photograph sits on warm paper with editorial copy.
3. **The table:** the supplied food creative sits in a terracotta field.
4. **The calendar:** event information appears on pale sage with oxblood dividers.
5. **Together:** the landscape reel moves into a deep oxblood evening band.
6. **Close:** the footer returns to olive with clear contact and location information.

## Visual system

- Canvas: champagne ivory `#F7F0E5`.
- Secondary canvas: parchment `#EEDFCC`.
- Ink: deep olive `#263027`.
- Quiet text: moss gray `#5C655E`.
- Primary action: oxblood `#7A3040`.
- Dining field: terracotta `#C76D49`.
- Event field: pale sage `#DCE3D3`.
- Accent: burnished brass `#9A641F`, reserved for focus, rules, and small labels.
- Dark media text: warm white `#FFF8EF`.
- Type: existing Playfair Display and DM Sans remain; scale and line length are corrected instead of adding another network dependency.
- Corners remain square. Depth comes from soft, offset shadows on media and active surfaces, never glow or glass.

## Interaction language

- No `↗`, `→`, `←`, `↑`, or `↓` glyphs.
- Buttons use clear labels: “Book a table,” “Explore the menu,” “Reserve,” “Previous,” “Next,” and “Back to top.”
- Text links use an animated underline and colour shift; primary actions use oxblood blocks.
- The one authored motion moment is the hero reel reveal, using clip-path and opacity from an already-visible default. Reduced motion disables it.
- Focus rings use brass with sufficient contrast. Selection, scrollbars, form controls, and hover states use the same palette.

## Cross-surface application

- Restaurant, events, private events, booking, and contact inherit the warm paper system, with dark treatment only where text overlays photography.
- The menu uses the light canvas around the existing illustrated dishes; category navigation remains a high-contrast olive band.
- Pickup ordering uses paper and parchment surfaces, olive text, oxblood actions, and a light cart drawer. Dish imagery and interaction behavior remain unchanged.

## Responsive and accessibility requirements

- No horizontal overflow at 390px.
- Touch targets remain at least 44px.
- Body text contrast is at least 4.5:1; large display text at least 3:1.
- Media retains useful crop at desktop and mobile.
- Keyboard navigation, visible focus, reduced motion, form validation, and dialog behavior remain intact.

## Verification

- Rendered public pages contain no Unicode arrow glyph controls.
- Homepage, menu, and pickup pages use a light body canvas.
- Homepage media remains limited to the four supplied assets.
- Full browser/site suite passes.
- Desktop and mobile screenshots are reviewed in one batched pass, followed by at most one correction pass.
