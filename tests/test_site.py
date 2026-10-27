import unittest
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1] / "dist"


class DebutSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def open_page(self, path="index.html", width=1440):
        page = self.browser.new_page(viewport={"width": width, "height": 900})
        page.goto((ROOT / path).as_uri())
        return page

    def test_homepage_has_full_restaurant_journey(self):
        page = self.open_page()
        self.assertTrue(page.get_by_role("heading", level=1).is_visible())
        for href in ("menu/", "events/", "restaurant/", "book/", "contact/"):
            self.assertGreater(page.locator(f'a[href="{href}"]').count(), 0, href)
        self.assertEqual(page.get_by_role("link", name="Order online", exact=False).first.get_attribute("href"), "order/")
        restaurant = self.open_page("restaurant/index.html")
        restaurant_photo = restaurant.locator(".interior-hero-image img").get_attribute("src").split("/")[-1]
        self.assertIn(restaurant_photo, page.locator(".hero-photograph").evaluate("el => getComputedStyle(el).backgroundImage"))
        restaurant.close()
        self.assertTrue(page.get_by_role("link", name="Staff login", exact=False).first.get_attribute("href").startswith("https://debutbar.ca/admin"))
        page.close()

    def test_homepage_leads_with_the_supplied_video_and_clear_actions(self):
        page = self.open_page()
        video = page.locator('.home-hero video')
        self.assertEqual(video.count(), 1)
        self.assertTrue(video.evaluate('el => el.autoplay && el.loop && el.muted && el.playsInline'))
        self.assertTrue(video.get_attribute('poster').endswith('debut-night-poster.webp'))
        self.assertTrue(video.locator('source').get_attribute('src').endswith('debut-night.mp4'))
        self.assertGreater(video.evaluate('el => el.videoWidth'), 0)
        self.assertGreater(page.locator('.home-hero a[href="book/"]').count(), 0)
        self.assertGreater(page.locator('.home-hero a[href="menu/"]').count(), 0)
        page.close()

    def test_homepage_uses_the_new_food_and_nightlife_media(self):
        page = self.open_page()
        food = page.locator('.menu-feature-art img')
        self.assertTrue(food.get_attribute('src').endswith('debut-food-feature.webp'))
        self.assertGreater(food.evaluate('image => image.naturalWidth'), 0)

        nightlife = page.locator('.private-feature video')
        self.assertEqual(nightlife.count(), 1)
        self.assertTrue(nightlife.evaluate('el => el.autoplay && el.loop && el.muted && el.playsInline'))
        self.assertTrue(nightlife.get_attribute('poster').endswith('debut-night-wide-poster.webp'))
        self.assertTrue(nightlife.locator('source').get_attribute('src').endswith('debut-night-wide.mp4'))
        self.assertGreater(nightlife.evaluate('el => el.videoWidth'), 0)
        page.close()

    def test_homepage_uses_only_the_supplied_media(self):
        page = self.open_page()
        self.assertEqual(
            page.locator('main img').evaluate_all(
                "images => images.map(image => image.getAttribute('src'))"
            ),
            ['media/restaurant-lounge.webp', 'media/debut-food-feature.webp'],
        )
        self.assertEqual(
            page.locator('main video source').evaluate_all(
                "sources => sources.map(source => source.getAttribute('src'))"
            ),
            ['media/debut-night.mp4', 'media/debut-night-wide.mp4'],
        )
        page.close()

    def test_homepage_video_and_actions_fit_mobile(self):
        page = self.open_page(width=390)
        self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), 390)
        video = page.locator('.home-hero video')
        self.assertTrue(video.is_visible())
        self.assertGreater(video.bounding_box()['height'], 300)
        self.assertTrue(page.locator('.home-hero a[href="book/"]').is_visible())
        self.assertTrue(page.locator('.home-hero a[href="menu/"]').is_visible())
        page.close()

    def test_homepage_video_respects_reduced_motion(self):
        page = self.browser.new_page(reduced_motion='reduce')
        page.goto((ROOT / 'index.html').as_uri())
        videos = page.locator('video')
        self.assertEqual(videos.count(), 2)
        self.assertTrue(all(videos.evaluate_all('elements => elements.map(el => el.paused)')))
        page.close()

    def test_every_route_uses_the_same_header_and_mobile_navigation(self):
        routes = ("index.html", "restaurant/index.html", "menu/index.html", "order/index.html", "events/index.html", "private-events/index.html", "book/index.html", "contact/index.html")
        expected = ["Home", "Restaurant", "Menu", "Pickup", "Events", "Contact", "Book a table"]
        for route in routes:
            page = self.open_page(route, width=390)
            self.assertEqual(page.locator("header.global-header").count(), 1, route)
            toggle = page.get_by_role("button", name="Open menu")
            toggle.click()
            links = page.locator("#global-nav a")
            self.assertEqual([text.strip() for text in links.all_text_contents()], expected, route)
            self.assertTrue(links.first.is_visible(), route)
            page.keyboard.press("Escape")
            self.assertFalse(links.first.is_visible(), route)
            if route == "order/index.html":
                page.get_by_role("button", name="View order").click()
                self.assertEqual(page.locator("#cart-drawer").get_attribute("aria-hidden"), "false")
            page.close()

    def test_every_route_uses_the_brand_favicon(self):
        routes = ("index.html", "restaurant/index.html", "menu/index.html", "order/index.html", "events/index.html", "private-events/index.html", "book/index.html", "contact/index.html")
        for route in routes:
            page = self.open_page(route)
            icon = page.locator('link[rel="icon"]')
            self.assertEqual(icon.count(), 1, route)
            self.assertTrue(icon.get_attribute("href").endswith("favicon.png"), route)
            self.assertEqual(icon.evaluate("el => new URL(el.href).pathname.split('/').pop()"), "favicon.png", route)
            page.close()
        self.assertLess((ROOT / "favicon.png").stat().st_size, 50000)

    def test_events_have_current_dates_and_reservation_action(self):
        page = self.open_page("events/index.html")
        self.assertTrue(page.get_by_text("October 2026", exact=False).first.is_visible())
        self.assertTrue(page.get_by_text("Wine Tasting", exact=False).first.is_visible())
        self.assertGreater(page.locator('a[href="../book/"]').count(), 0)
        poster = page.locator(".events-hero .event-poster img")
        self.assertEqual(poster.count(), 1)
        self.assertTrue(poster.is_visible())
        self.assertGreater(poster.evaluate("image => image.naturalWidth"), 0)
        page.close()
        page = self.open_page("events/index.html", width=390)
        self.assertGreater(page.locator(".events-hero-image").evaluate("element => element.getBoundingClientRect().height"), 500)
        page.close()

    def test_october_event_artwork_retires_after_month_in_barrie(self):
        page = self.browser.new_page(viewport={"width": 390, "height": 900})
        page.add_init_script("""(() => {
          const ActualDate = Date;
          window.Date = class extends ActualDate {
            constructor(...args) { super(...(args.length ? args : ['2026-11-02T15:00:00Z'])); }
            static now() { return new ActualDate('2026-11-02T15:00:00Z').getTime(); }
          };
        })()""")
        page.goto((ROOT / "events" / "index.html").as_uri())
        self.assertFalse(page.locator(".event-poster").is_visible())
        self.assertFalse(page.locator("#dates").is_visible())
        self.assertFalse(page.locator(".event-banner").is_visible())
        self.assertTrue(page.get_by_role("link", name="Latest on Instagram", exact=False).is_visible())
        self.assertTrue(page.locator(".weekly-program").is_visible())
        page.close()

    def test_october_events_remain_on_october_31_in_barrie(self):
        page = self.browser.new_page(viewport={"width": 1440, "height": 900})
        page.add_init_script("""(() => {
          const ActualDate = Date;
          window.Date = class extends ActualDate {
            constructor(...args) { super(...(args.length ? args : ['2026-11-01T02:00:00Z'])); }
            static now() { return new ActualDate('2026-11-01T02:00:00Z').getTime(); }
          };
        })()""")
        page.goto((ROOT / "events" / "index.html").as_uri())
        self.assertTrue(page.locator(".event-poster").is_visible())
        self.assertTrue(page.locator(".event-row[data-date='2026-10-31']").is_visible())
        page.close()

    def test_booking_uses_direct_contact_until_reservations_are_private(self):
        page = self.open_page("book/index.html")
        self.assertEqual(page.locator('a[href="https://debutbar.ca/book"]').count(), 0)
        self.assertEqual(page.get_by_role("link", name="Call to reserve", exact=False).get_attribute("href"), "tel:+19428833288")
        self.assertTrue(page.get_by_role("link", name="Email the team", exact=False).get_attribute("href").startswith("mailto:info@debutbar.ca"))
        page.close()
        page = self.open_page("contact/index.html")
        self.assertGreater(page.locator('a[href="mailto:info@debutbar.ca"]').count(), 0)
        self.assertGreater(page.locator('a[href^="tel:"]').count(), 0)
        self.assertIn("10 Dunlop St E", page.locator("body").inner_text())
        page.close()

    def test_mobile_navigation_opens_without_overflow(self):
        page = self.open_page(width=390)
        page.get_by_role("button", name="Open menu").click()
        self.assertTrue(page.get_by_role("navigation", name="Main navigation").get_by_role("link", name="Events", exact=True).is_visible())
        self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 390)
        page.close()

    def test_official_logo_is_used_in_header_and_footer(self):
        for path in ("index.html", "menu/index.html"):
            page = self.open_page(path)
            header = page.locator(".global-brand img")
            footer = page.locator(".footer-logo img")
            self.assertEqual(header.count(), 1, path)
            self.assertEqual(footer.count(), 1, path)
            self.assertGreater(header.evaluate("image => image.naturalWidth"), 0)
            self.assertGreater(footer.evaluate("image => image.naturalWidth"), 0)
            page.close()

    def test_private_events_have_a_dedicated_inquiry_journey(self):
        home = self.open_page()
        self.assertGreater(home.locator('a[href="private-events/"]').count(), 0)
        home.close()
        page = self.open_page("private-events/index.html", width=390)
        text = page.locator("main").inner_text()
        self.assertIn("Semi-private", text)
        self.assertIn("Full venue", text)
        self.assertIn("custom menus", text.lower())
        inquiry = page.get_by_role("link", name="Ask about your event", exact=False)
        self.assertTrue(inquiry.get_attribute("href").startswith("mailto:info@debutbar.ca?subject="))
        self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 390)
        page.close()


if __name__ == "__main__":
    unittest.main()
