import json
import unittest
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
MENU = json.loads((ROOT / "menu.json").read_text())


class OrderingExperienceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def test_homepage_leads_with_restaurant_and_links_to_ordering(self):
        page = self.browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto((ROOT / "dist" / "index.html").as_uri())
        self.assertTrue(page.locator(".home-hero").is_visible())
        self.assertIn("The night", page.get_by_role("heading", level=1).inner_text())
        self.assertEqual(page.locator("#featured-image").count(), 0)
        self.assertGreater(page.locator('a[href="order/"]').count(), 0)
        page.close()

    def test_menu_products_and_cart_math(self):
        page = self.browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto((ROOT / "dist" / "order" / "index.html").as_uri())
        self.assertTrue(page.get_by_role("heading", name="Order for pickup").is_visible())
        self.assertEqual(page.locator(".dish-rail button[data-item-id]").count(), sum(
            isinstance(item.get("price"), (int, float))
            for section in MENU["sections"] if section["id"] not in ("deals", "add-ons")
            for item in section["items"]
        ))
        self.assertIn("Butter Chicken Poutine", page.locator("#featured-name").inner_text())
        page.get_by_role("button", name="Add Butter Chicken Poutine to order").click()
        page.get_by_role("button", name="View order").click()
        self.assertIn("$15.00", page.locator("#cart-subtotal").inner_text())
        self.assertIn("$1.95", page.locator("#cart-tax").inner_text())
        self.assertIn("$16.95", page.locator("#cart-total").inner_text())
        page.get_by_role("button", name="Increase Butter Chicken Poutine quantity").click()
        self.assertIn("$30.00", page.locator("#cart-subtotal").inner_text())
        page.close()

    def test_keyboard_navigation_and_mobile_layout(self):
        page = self.browser.new_page(viewport={"width": 390, "height": 844})
        page.goto((ROOT / "dist" / "order" / "index.html").as_uri())
        page.keyboard.press("ArrowRight")
        self.assertIn("Chicken Quesadilla", page.locator("#featured-name").inner_text())
        self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 390)
        page.close()

    def test_add_to_cart_flight_stays_visible_on_mobile(self):
        page = self.browser.new_page(viewport={"width": 390, "height": 844})
        page.goto((ROOT / "dist" / "order" / "index.html").as_uri())
        page.get_by_role("button", name="Add Butter Chicken Poutine to order").click()
        cart = page.get_by_role("button", name="View order").bounding_box()
        flight = page.locator(".fly-dish").bounding_box()
        self.assertGreaterEqual(cart["y"], 0)
        self.assertGreaterEqual(flight["y"] + flight["height"], 0)
        self.assertLess(flight["y"], 844)
        page.wait_for_timeout(1000)
        self.assertEqual(page.locator(".fly-dish").count(), 0)
        self.assertEqual(page.locator("#cart-count").inner_text(), "1")
        page.close()

    def test_checkout_is_request_and_requires_restaurant_confirmation(self):
        page = self.browser.new_page()
        page.goto((ROOT / "dist" / "order" / "index.html").as_uri())
        page.get_by_role("button", name="Add Butter Chicken Poutine to order").click()
        page.get_by_role("button", name="View order").click()
        self.assertIn("request", page.locator("#order-form").inner_text().lower())
        self.assertIn("confirm", page.locator("#order-form").inner_text().lower())
        self.assertEqual(page.locator("#order-form input[required]").count(), 4)
        page.close()

    def test_pickup_submission_sends_complete_order_and_clears_cart_on_success(self):
        page = self.browser.new_page()
        payloads = []
        def formspree(route):
            payloads.append(route.request.post_data_json)
            route.fulfill(status=200, content_type="application/json", headers={"access-control-allow-origin": "*"}, body='{"ok":true}')
        page.route("https://formspree.io/f/mnpjboyk", formspree)
        page.goto((ROOT / "dist" / "order" / "index.html").as_uri())
        page.get_by_role("button", name="Add Butter Chicken Poutine to order").click()
        page.get_by_role("button", name="View order").click()
        page.locator('[name="name"]').fill("Alex Test")
        page.locator('[name="email"]').fill("alex@example.com")
        page.locator('[name="phone"]').fill("7055551234")
        page.locator('[name="date"]').fill(page.locator('[name="date"]').get_attribute("min"))
        page.locator('[name="time"]').select_option("18:00")
        page.locator('[name="notes"]').fill("No peanuts")
        page.locator('#order-form button[type="submit"]').click()
        page.get_by_role("heading", name="Request sent.").wait_for()
        self.assertEqual(len(payloads), 1)
        self.assertEqual(payloads[0]["email"], "alex@example.com")
        self.assertEqual(payloads[0]["items"][0]["name"], "Butter Chicken Poutine")
        self.assertEqual(payloads[0]["items"][0]["quantity"], 1)
        self.assertEqual(payloads[0]["estimated_total"], "$16.95")
        self.assertEqual(payloads[0]["notes"], "No peanuts")
        self.assertEqual(page.locator("#cart-count").inner_text(), "0")
        page.close()

    def test_failed_pickup_submission_preserves_cart_and_shows_email_fallback(self):
        page = self.browser.new_page()
        page.route("https://formspree.io/f/mnpjboyk", lambda route: route.fulfill(status=500, content_type="application/json", headers={"access-control-allow-origin": "*"}, body='{"error":"unavailable"}'))
        page.goto((ROOT / "dist" / "order" / "index.html").as_uri())
        page.get_by_role("button", name="Add Butter Chicken Poutine to order").click()
        page.get_by_role("button", name="View order").click()
        page.locator('[name="name"]').fill("Alex Test")
        page.locator('[name="email"]').fill("alex@example.com")
        page.locator('[name="phone"]').fill("7055551234")
        page.locator('[name="date"]').fill(page.locator('[name="date"]').get_attribute("min"))
        page.locator('[name="time"]').select_option("18:00")
        page.locator('#order-form button[type="submit"]').click()
        page.get_by_text("Could not send your request.", exact=False).wait_for()
        self.assertEqual(page.locator("#cart-count").inner_text(), "1")
        self.assertTrue(page.locator("#order-form").is_visible())
        self.assertTrue(page.locator("#email-link").is_visible())
        self.assertTrue(page.locator("#email-link").get_attribute("href").startswith("mailto:info@debutbar.ca"))
        page.close()


if __name__ == "__main__":
    unittest.main()
