"""Build the public Début pages around the existing illustrated menu."""

from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
INSTAGRAM = "https://www.instagram.com/debutbar.ca/"
FACEBOOK = "https://www.facebook.com/profile.php?id=61581988111686"


def nav(prefix="", active="", cart=False):
    links = [("Home", "index.html"), ("Restaurant", "restaurant/"), ("Menu", "menu/"), ("Pickup", "order/"), ("Events", "events/"), ("Contact", "contact/"), ("Book a table", "book/")]
    items = "".join(
        f'<a href="{prefix}{href}"{(" class=\"nav-book\"" if label == "Book a table" else "")}{(" aria-current=\"page\"" if active == label else "")}>{label}</a>'
        for label, href in links
    )
    cart_button = '<button id="open-cart" class="cart-trigger" type="button" aria-label="View order"><span>Your order</span><span id="cart-count" class="cart-count">0</span><span aria-hidden="true">↗</span></button>' if cart else ''
    return f'''<header class="global-header" id="site-top">
      <a class="global-brand" href="{prefix}index.html" aria-label="Début home"><span class="brand-logo-mark"><img src="{prefix}media/debut-logo.png" alt="" width="3785" height="3706"></span><span>DÉBUT<small>BAR & RESTAURANT</small></span></a>
      <nav class="global-nav" id="global-nav" aria-label="Main navigation">{items}</nav>
      <div class="header-actions">{cart_button}<a class="order-link" href="{prefix}order/">Order online ↗</a><a class="reserve-link" href="{prefix}book/"{(" aria-current=\"page\"" if active == "Book a table" else "")}>Book a table <span aria-hidden="true">↗</span></a></div>
      <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="global-nav"><span></span><span></span></button>
    </header>'''


def footer(prefix=""):
    return f'''<footer class="global-footer">
      <div class="footer-top"><div><p class="section-kicker">DÉBUT · BARRIE</p><h2>Your table<br><em>is waiting.</em></h2></div><a class="footer-book" href="{prefix}book/">Reserve your table <span aria-hidden="true">↗</span></a></div>
      <div class="footer-grid"><div><a class="footer-logo" href="{prefix}index.html"><img src="{prefix}media/debut-logo.png" alt="Début Bar & Restaurant" width="3785" height="3706" loading="lazy"></a><p>10 Dunlop St E<br>Barrie, ON L4M 1A3</p></div><div><span class="footer-label">EXPLORE</span><a href="{prefix}restaurant/">Restaurant</a><a href="{prefix}menu/">Menu</a><a href="{prefix}events/">Events</a><a href="{prefix}private-events/">Private events</a><a href="{prefix}contact/">Contact</a></div><div><span class="footer-label">CONNECT</span><a href="mailto:info@debutbar.ca">info@debutbar.ca</a><a href="tel:+19428833288">+1 942 883 3288</a><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">Instagram ↗</a><a href="{FACEBOOK}" target="_blank" rel="noopener noreferrer">Facebook ↗</a></div><div><span class="footer-label">VISIT</span><a href="https://www.google.com/maps/search/?api=1&query=10+Dunlop+St+E%2C+Barrie%2C+ON+L4M+1A3" target="_blank" rel="noopener noreferrer">Get directions ↗</a><a href="{prefix}order/">Order online ↗</a><a href="https://debutbar.ca/admin" target="_blank" rel="noopener noreferrer">Staff login ↗</a></div></div>
      <div class="footer-bottom"><span>© DÉBUT BAR & RESTAURANT</span><span>BARRIE, ONTARIO · CANADA</span><a href="#site-top">BACK TO TOP ↑</a></div>
    </footer>'''


def page(title, description, body, route="", kind=""):
    prefix = "../" if route else ""
    return dedent(f'''<!doctype html>
    <html lang="en"><head>
      <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
      <meta name="theme-color" content="#121412"><meta name="description" content="{description}">
      <title>{title} | DÉBUT Bar & Restaurant</title>
      <link rel="icon" type="image/png" href="{prefix}favicon.png">
      <link rel="apple-touch-icon" href="{prefix}apple-touch-icon.png">
      <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet">
      <link rel="stylesheet" href="{prefix}site.css"><script defer src="{prefix}site.js"></script>
    </head><body class="full-site {kind}"><a class="skip-link" href="#main">Skip to content</a>
    {nav(prefix, "Home" if not route else ("Book a table" if route == "book" else title if title in ("Restaurant", "Events", "Contact") else ""))}
    <main id="main">{body}</main>{footer(prefix)}</body></html>''')


home = '''
<section class="home-hero" aria-labelledby="home-title"><div class="hero-photograph" role="img" aria-label="The lounge inside Début Bar and Restaurant"></div><div class="hero-video"><video autoplay muted loop playsinline preload="metadata" poster="media/debut-night-poster.webp" aria-label="A night out at Début Bar and Restaurant"><source src="media/debut-night.mp4" type="video/mp4"></video><span class="hero-video-label">DÉBUT · BARRIE AFTER DARK</span></div><div class="home-hero-shade"></div><div class="home-hero-content"><p class="section-kicker"><span class="kicker-line"></span> DÉBUT · DOWNTOWN BARRIE</p><h1 id="home-title">THE NIGHT<br><em>IS YOURS.</em></h1><p>Dinner, cocktails and music. Make a night of it at Début.</p><div class="hero-actions"><a class="button-gold" href="book/">Book a table <span>↗</span></a><a class="button-outline" href="menu/">Explore the menu <span>↗</span></a></div></div><div class="hero-bottom"><span>10 DUNLOP ST E · BARRIE, ONTARIO</span><a href="#introduction">EXPLORE DÉBUT ↓</a></div></section>
<section class="intro-section section-frame" id="introduction"><div class="intro-heading"><h2>Come for dinner.<br><em>Stay for the night.</em></h2></div><div class="intro-right"><p>Start at the table, settle in at the bar, and see where the evening takes you. Début brings dining and nightlife together in downtown Barrie.</p><a class="arrow-link" href="restaurant/">Step inside <span>↗</span></a></div></section>
<section class="experience-grid section-frame" aria-label="The Début experience"><div class="experience-photo experience-photo-wide"><img src="media/restaurant-lounge.webp" alt="Black booth seating inside Début Bar and Restaurant" loading="lazy"><span class="photo-caption">01 — THE ROOM</span></div><div class="experience-copy"><h3>Dinner flows<br><em>into the night.</em></h3><p>Booth seating, a lit bar and space to stay after dinner.</p></div></section>
<section class="menu-feature section-frame"><div class="feature-copy"><p class="section-kicker">FOOD & DRINKS</p><h2>Made for<br><em>the moment.</em></h2><p>Bar snacks, shareable plates, dinner favourites and cocktails. Find your next order.</p><a class="button-outline" href="menu/">View the menu <span>↗</span></a></div><div class="menu-feature-art"><img src="media/debut-food-feature.webp" alt="Burger, ribs and grilled chicken served at Début" loading="lazy"></div></section>
<section class="events-feature section-frame"><div class="events-head"><div><p class="section-kicker">WHAT'S HAPPENING</p><h2>On the<br><em>calendar.</em></h2></div><a class="arrow-link" href="events/">All events <span>↗</span></a></div><div class="event-preview-grid"><a href="events/" class="event-preview" data-date="2026-10-14"><span class="event-date">14 <small>OCT</small></span><span><small>WEDNESDAY · 6–8 PM</small><strong>Wine Tasting</strong><em>with Trent Mayers</em></span><span class="event-arrow">↗</span></a><a href="events/" class="event-preview" data-date="2026-10-16"><span class="event-date">16 <small>OCT</small></span><span><small>FRIDAY · 6–9 PM</small><strong>Live Music</strong><em>with Jeff</em></span><span class="event-arrow">↗</span></a><a href="events/" class="event-preview" data-date="2026-10-31"><span class="event-date">31 <small>OCT</small></span><span><small>SATURDAY</small><strong>Halloween Party</strong><em>A night to remember</em></span><span class="event-arrow">↗</span></a><p class="no-event-previews" hidden>See the latest announcements on <a href="https://www.instagram.com/debutbar.ca/" target="_blank" rel="noopener noreferrer">Début's Instagram ↗</a></p></div></section>
<section class="private-feature"><video autoplay muted loop playsinline preload="metadata" poster="media/debut-night-wide-poster.webp" aria-label="Guests arriving and dining at Début"><source src="media/debut-night-wide.mp4" type="video/mp4"></video><div class="private-shade"></div><div class="private-content"><p class="section-kicker">MAKE IT YOURS</p><h2>Bring everyone<br><em>together.</em></h2><p>Bring your people together at Début. Ask us about private celebrations and corporate events.</p><a class="button-gold" href="private-events/">Plan an event <span>↗</span></a></div></section>
'''

restaurant = '''
<section class="interior-hero"><div class="interior-hero-image"><img src="../media/restaurant-lounge.webp" alt="Début's textured lounge and intimate seating"></div><div class="interior-hero-copy"><p class="section-kicker">10 DUNLOP ST E · DOWNTOWN BARRIE</p><h1>Our<br><em>restaurant.</em></h1><p>In the heart of downtown Barrie, the mood shifts as the evening unfolds.</p></div><span class="hero-route">THE EXPERIENCE / 01</span></section>
<section class="story-lead section-frame"><h2>A place to arrive.<br><em>A reason to stay.</em></h2><p>Come for a dinner date, bring friends for drinks or stay for live music. The dining room and bar share one evening.</p></section>
<section class="story-block section-frame"><div class="story-image tall"><img src="../media/restaurant-room.webp" alt="Début dining room with illuminated ceiling" loading="lazy"><span>01 / THE ROOM</span></div><div class="story-text"><p class="section-kicker">THE EXPERIENCE</p><h2>Find your<br><em>seat.</em></h2><p>Choose a booth, a dining table or a seat near the bar. The lights stay low as the evening picks up.</p><a class="arrow-link" href="../book/">Reserve a table <span>↗</span></a></div></section>
<section class="story-block story-block-reverse section-frame"><div class="story-image"><img src="../media/restaurant-bar.webp" alt="Début bar with illuminated counter and seating" loading="lazy"><span>02 / THE BAR</span></div><div class="story-text"><p class="section-kicker">BEHIND THE BAR</p><h2>Stay for<br><em>another round.</em></h2><p>Cocktails, wine and beer are served alongside the full food menu.</p><a class="arrow-link" href="../menu/">View food & drinks <span>↗</span></a></div></section>
<section class="restaurant-closing"><img src="../media/restaurant-arch.webp" alt="Début's signature illuminated arches" loading="lazy"><div><p class="section-kicker">YOUR NEXT OCCASION</p><h2>Make the room<br><em>your own.</em></h2><p>From private celebrations to corporate evenings, we would love to hear what you have in mind.</p><a class="button-gold" href="../private-events/">Explore private events <span>↗</span></a></div></section>
'''

private_events = '''
<section class="pe-hero"><div class="pe-hero-copy"><p class="section-kicker">DÉBUT · PRIVATE EVENTS</p><h1>A room for<br><em>your occasion.</em></h1><p>Celebrate, launch or bring the team together in the heart of downtown Barrie.</p><a class="button-gold" href="#inquiry">Plan your event <span>↓</span></a></div><div class="pe-hero-image"><img src="../media/restaurant-room.webp" alt="Dining tables inside Début Bar and Restaurant"></div></section>
<section class="pe-intro section-frame"><h2>Semi-private.<br>Or the whole venue.</h2><p>Tell the team your preferred date and approximate guest count. They can discuss a format that suits your gathering.</p></section>
<section class="pe-options section-frame" aria-label="Private event formats"><article><img src="../media/restaurant-lounge.webp" alt="Lounge seating inside Début" loading="lazy"><div><span>01 / SEMI-PRIVATE</span><h2>Semi-private gatherings</h2><p>Keep your group close while enjoying the energy of the restaurant and bar.</p></div></article><article><img src="../media/restaurant-detail.webp" alt="Début interior prepared for an evening event" loading="lazy"><div><span>02 / FULL VENUE</span><h2>Full venue bookings</h2><p>Make the entire room your own for a celebration, corporate gathering or launch.</p></div></article></section>
<section class="pe-table"><div><p class="section-kicker">FOOD & DRINKS</p><h2>The menu is<br>part of the night.</h2><p>Ask about custom menus and dedicated service for your event. Browse the current food and drinks to start planning.</p><a class="arrow-link" href="../menu/">Explore food & drinks <span>↗</span></a></div><img src="../media/restaurant-bar.webp" alt="The bar at Début illuminated for evening service" loading="lazy"></section>
<section class="pe-inquiry section-frame" id="inquiry"><div><p class="section-kicker">LET'S TALK</p><h2>Tell us what<br>you're planning.</h2></div><div><p>Share your preferred date, approximate guest count and the kind of event you have in mind. The team will discuss availability and details with you.</p><a class="button-gold" href="mailto:info@debutbar.ca?subject=Private%20event%20at%20D%C3%A9but">Ask about your event <span>↗</span></a><a class="pe-phone" href="tel:+19428833288">Or call +1 942 883 3288</a></div></section>
'''

EVENTS = [
    (14, "WED", "Wine Tasting", "with Trent Mayers", "6–8 PM"),
    (16, "FRI", "Live Music", "Jeff", "6–9 PM"),
    (17, "SAT", "Live Music", "Kat Chabot", "6–10 PM"),
    (22, "THU", "Karaoke", "with ZeBruh", "7 PM onwards"),
    (23, "FRI", "Live Music", "Brigitte and Eve", "6–9 PM"),
    (24, "SAT", "Live Music", "Artist to be announced", "6–9 PM"),
    (28, "WED", "Sip & Paint", "with artist Namrata", "6–8 PM"),
    (30, "FRI", "Live Music", "Kat Chabot", "6–10 PM"),
    (31, "SAT", "Halloween Party", "Celebrate with us", "Time to be announced"),
]


def event_rows():
    return "".join(
        f'<article class="event-row" data-date="2026-10-{day:02d}"><div class="event-row-date"><strong>{day:02d}</strong><span>OCT / {weekday}</span></div><div class="event-row-title"><h3>{name}</h3><p>{subtitle}</p></div><div class="event-row-time">{time}</div><a href="../book/" aria-label="Book a table for {name} on October {day}">↗</a></article>'
        for day, weekday, name, subtitle, time in EVENTS
    )


events = f'''
<section class="events-hero"><div class="events-hero-copy"><p class="section-kicker">THE CALENDAR</p><h1 id="events-title">October at<br><em>Début.</em></h1><p id="events-intro">Wine tasting, live music, karaoke, Sip & Paint and a Halloween party.</p><a class="button-gold" id="events-hero-cta" href="#dates">Explore the dates <span>↓</span></a></div><div class="events-hero-image"><img class="events-room" src="../media/restaurant-detail.webp" alt="" aria-hidden="true"><figure class="event-poster"><img src="../media/debut-event-original.jpg" alt="Début October 2026 event calendar poster" width="1122" height="1402"></figure></div><span class="events-hero-index">DÉBUT / AFTER DARK</span></section>
<section class="event-list-section section-frame" id="dates"><div class="events-list-heading"><div><p class="section-kicker">WHAT'S ON</p><h2>October <em>2026.</em></h2></div><p>Select an event below. Confirm details with the team before visiting.</p></div><div id="event-list">{event_rows()}</div><p class="no-events" hidden>The October 2026 calendar has ended. Follow <a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">Début on Instagram ↗</a> for the latest dates.</p></section>
<section class="weekly-program section-frame"><div><p class="section-kicker">THE WEEKLY RHYTHM</p><h2>Every week<br><em>at Début.</em></h2><p class="weekly-latest" hidden>Programming may change. See <a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">the latest announcements ↗</a>.</p></div><div class="weekly-list"><div><span>WED</span><h3>Wine Night</h3><p>Wine and good company on Wednesdays.</p></div><div><span>FRI</span><h3>DJ Night</h3><p>EDM and house into the early hours.</p></div><div><span>SAT</span><h3>Saturday Nights</h3><p>Music into the weekend.</p></div></div></section>
<section class="event-banner"><img src="../media/debut-event-original.jpg" alt="Début October 2026 event calendar poster" loading="lazy"><div><p class="section-kicker">COME TOGETHER</p><h2>See you<br><em>in October.</em></h2><p>Browse the full October poster and reserve your table.</p><a class="button-outline" href="../book/">Reserve a table <span>↗</span></a></div></section>
'''

book = '''
<section class="booking-hero"><div class="booking-copy"><p class="section-kicker">A SEAT AT DÉBUT</p><h1>Reserve<br><em>your table.</em></h1><p>Make plans for dinner, a celebration or an evening out. Reach the Début team directly to request your table.</p><div class="booking-card"><span class="booking-card-number">01 / YOUR RESERVATION</span><h2>Book directly with the team.</h2><p>Call or email with your preferred date, time, party size and contact number. The team will confirm availability with you. Début is closed on Tuesdays.</p><div class="booking-card-actions"><a class="button-gold" href="tel:+19428833288">Call to reserve <span>↗</span></a><a class="button-outline" href="mailto:info@debutbar.ca?subject=Table%20reservation%20at%20D%C3%A9but">Email the team <span>↗</span></a></div><small>A request is confirmed only after the team replies.</small></div></div><div class="booking-image"><img src="../media/restaurant-arch.webp" alt="The illuminated entrance to Début's dining room"></div></section>
<section class="booking-form-section section-frame" aria-labelledby="reserve-heading"><div class="reserve-form-intro"><p class="section-kicker">RESERVE A TABLE</p><h2 id="reserve-heading">Request<br><em>your table.</em></h2><p>Fill in your details and preferred time. Your request is sent directly to the team — nothing is booked until they confirm.</p></div><div class="reserve-form-wrap"><form id="reserve-form" action="https://formspree.io/f/mnpjboyk" method="POST" novalidate><div class="reserve-grid"><div class="field"><label for="res-name">Full name</label><input id="res-name" name="name" type="text" autocomplete="name" placeholder="Jane Doe" required minlength="2" maxlength="100"><p class="field-error" id="err-res-name" hidden>Name must be at least 2 characters</p></div><div class="field"><label for="res-email">Email address</label><input id="res-email" name="email" type="email" autocomplete="email" placeholder="jane@example.com" required maxlength="254"><p class="field-error" id="err-res-email" hidden>Invalid email address</p></div><div class="field"><label for="res-phone">Phone number</label><input id="res-phone" name="phone" type="tel" autocomplete="tel" placeholder="(705) 555-0123" required maxlength="30"><p class="field-error" id="err-res-phone" hidden>Phone number must be at least 10 digits</p></div><div class="field field-row"><div><label for="res-date">Date</label><input id="res-date" name="date" type="date" required><p class="field-error" id="err-res-date" hidden>Date is required</p></div><div><label for="res-time">Time</label><input id="res-time" name="time" type="time" required><p class="field-error" id="err-res-time" hidden>Time is required</p></div></div><div class="field"><label for="res-guests">Guests</label><select id="res-guests" name="guests" required><option value="1">1 guest</option><option value="2" selected>2 guests</option><option value="3">3 guests</option><option value="4">4 guests</option><option value="5">5 guests</option><option value="6">6 guests</option><option value="7">7 guests</option><option value="8">8 guests</option><option value="9">9 guests</option><option value="10">10 guests</option><option value="11">11 guests</option><option value="12">12 guests</option><option value="13">13 guests</option><option value="14">14 guests</option><option value="15">15 guests</option><option value="16">16 guests</option><option value="17">17 guests</option><option value="18">18 guests</option><option value="19">19 guests</option><option value="20">20 guests</option></select><p class="field-error" id="err-res-guests" hidden>Select 1–20 guests</p></div><div class="field"><label for="res-message">Special requests <span class="optional">(optional)</span></label><textarea id="res-message" name="message" rows="4" maxlength="1000" placeholder="Birthday, high chair, allergies…"></textarea></div></div><p class="form-status" id="reserve-status" role="status" aria-live="polite" hidden></p><div class="reserve-actions"><button class="button-gold" type="submit">Request table <span>↗</span></button><a class="button-outline" id="reserve-mailto" href="mailto:info@debutbar.ca?subject=Table%20reservation%20at%20D%C3%A9but" hidden>Email instead <span>↗</span></a></div><small class="reserve-note">Closed on Tuesdays. A request is confirmed only after the team replies.</small></form></div></section>
<section class="booking-details section-frame"><div><span class="ornament">✦</span><h2>Planning a<br><em>larger gathering?</em></h2></div><div><p>Planning a group dinner, private celebration or corporate event? Reach out and tell us what you are imagining.</p><a class="arrow-link" href="../private-events/">Explore private events <span>↗</span></a></div></section>
'''

contact = f'''
<section class="contact-hero"><div class="contact-copy"><p class="section-kicker">VISIT US / GET IN TOUCH</p><h1>Let's make<br><em>plans.</em></h1><p>Find us in downtown Barrie or get in touch about a booking or event.</p><div class="contact-list"><div><span>01 / FIND US</span><address>10 Dunlop St E<br>Barrie, ON L4M 1A3</address><a href="https://www.google.com/maps/search/?api=1&query=10+Dunlop+St+E%2C+Barrie%2C+ON+L4M+1A3" target="_blank" rel="noopener noreferrer">Get directions ↗</a></div><div><span>02 / SAY HELLO</span><a class="contact-primary" href="mailto:info@debutbar.ca">info@debutbar.ca</a><a href="tel:+19428833288">+1 942 883 3288</a></div><div><span>03 / FOLLOW ALONG</span><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">Instagram ↗</a><a href="{FACEBOOK}" target="_blank" rel="noopener noreferrer">Facebook ↗</a></div></div></div><div class="contact-photos"><img src="../media/restaurant-room.webp" alt="Inside Début Bar and Restaurant" class="contact-photo-main"><img src="../media/restaurant-arch.webp" alt="The illuminated arches at Début" class="contact-photo-small"></div></section>
<section class="contact-final section-frame"><p class="section-kicker">COME BY</p><h2>We'll see you<br><em>at Début.</em></h2><a class="button-gold" href="../book/">Book a table <span>↗</span></a></section>
'''


def build_menu():
    source = (ROOT / "menu-page.html").read_text(encoding="utf-8")
    source = source.replace('href="style.css"', 'href="../style.css"><link rel="stylesheet" href="../site.css"')
    source = source.replace('src="menu-data.js"', 'src="../menu-data.js"')
    source = source.replace('src="app.js"', 'src="../app.js"')
    source = source.replace('</head>', '<script>window.DEBUT_ASSET_PREFIX="../";</script><script defer src="../site.js"></script></head>')
    source = source.replace('href="DEBUT-3D-Menu-Print.pdf"', 'href="../DEBUT-3D-Menu-Print.pdf"')
    source = source.replace('src="images/generated/appetizers-01.webp"', 'src="../images/generated/appetizers-01.webp"')
    source = source.replace('src="scan-menu-qr.png"', 'src="../scan-menu-qr.png"')
    source = source.replace('<body>', '<body class="menu-page">')
    source = source.replace('href="favicon.png"', 'href="../favicon.png"', 1)
    source = source.replace('href="apple-touch-icon.png"', 'href="../apple-touch-icon.png"', 1)
    source = source.replace('<!-- SITE_HEADER -->', nav("../", "Menu"), 1)
    source = source.replace('</main>', '</main>' + footer("../"), 1)
    source = source.replace('href="https://benzom666.github.io/debut-3d-menu-temp/#appetizers"', 'href="https://benzom666.github.io/debut-3d-menu-temp/menu/#appetizers"')
    target = DIST / "menu" / "index.html"
    target.parent.mkdir(exist_ok=True)
    target.write_text(source, encoding="utf-8")


def main():
    pages = [
        ("", "Début Bar & Restaurant", "Dinner, cocktails and nights to remember in downtown Barrie, Ontario.", home, "home-page"),
        ("restaurant", "Restaurant", "Explore the dining room, bar and atmosphere at Début Bar & Restaurant in Barrie.", restaurant, "restaurant-page"),
        ("private-events", "Private Events", "Host a semi-private gathering or full venue event at Début Bar & Restaurant in downtown Barrie.", private_events, "private-events-page"),
        ("events", "Events", "Live music, karaoke, wine tastings and more at Début Bar & Restaurant in Barrie.", events, "events-page"),
        ("book", "Book a Table", "Request a table at Début Bar & Restaurant in downtown Barrie.", book, "book-page"),
        ("contact", "Contact", "Visit Début Bar & Restaurant at 10 Dunlop St E, Barrie, Ontario, or get in touch with our team.", contact, "contact-page"),
    ]
    for route, title, description, body, kind in pages:
        folder = DIST / route if route else DIST
        folder.mkdir(exist_ok=True)
        (folder / "index.html").write_text(page(title, description, body, route, kind), encoding="utf-8")
    build_menu()
    order = DIST / "order"
    order.mkdir(exist_ok=True)
    order_html = (ROOT / "order-page.html").read_text(encoding="utf-8")
    order_html = order_html.replace('<!-- SITE_HEADER -->', nav("../", "Pickup", cart=True), 1)
    order_html = order_html.replace('</head>', '<script defer src="../site.js"></script></head>', 1)
    order_html = order_html.replace("</main>", "</main>" + footer("../"), 1)
    (order / "index.html").write_text(order_html, encoding="utf-8")
    print("Built homepage, restaurant, private events, events, booking, contact, menu, and pickup")


if __name__ == "__main__":
    main()
