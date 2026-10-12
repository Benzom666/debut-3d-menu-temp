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
        self.assertTrue(page.get_by_role("link", name="Staff login", exact=False).first.get_attribute("href").startswith("https://debutbar.ca/admin"))
        page.close()

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
