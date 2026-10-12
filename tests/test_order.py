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

    def test_homepage_features_generated_dishes_and_side_list(self):
        page = self.browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto((ROOT / "dist" / "index.html").as_uri())
        self.assertEqual(page.locator(".dish-rail button[data-item-id]").count(), 66)
        self.assertIn("images/generated/appetizers-01.webp", page.locator("#featured-image").get_attribute("src"))
        self.assertTrue(page.locator(".dish-browser").is_visible())
        page.keyboard.press("ArrowRight")
        self.assertIn("Chicken Quesadilla", page.locator("#featured-name").inner_text())
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

    def test_checkout_is_request_and_requires_restaurant_confirmation(self):
        page = self.browser.new_page()
        page.goto((ROOT / "dist" / "order" / "index.html").as_uri())
        page.get_by_role("button", name="Add Butter Chicken Poutine to order").click()
        page.get_by_role("button", name="View order").click()
        self.assertIn("request", page.locator("#order-form").inner_text().lower())
        self.assertIn("confirm", page.locator("#order-form").inner_text().lower())
        self.assertEqual(page.locator("#order-form input[required]").count(), 4)
        page.close()


if __name__ == "__main__":
    unittest.main()
