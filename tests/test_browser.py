import json
import unittest
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
MENU = json.loads((ROOT / "menu.json").read_text())


class BrowserMenuTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def test_every_section_and_item_is_readable(self):
        page = self.browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto((ROOT / "dist" / "menu" / "index.html").as_uri())
        self.assertEqual(page.locator(".menu-section").count(), len(MENU["sections"]))
        self.assertEqual(page.locator(".menu-item").count(), sum(len(s["items"]) for s in MENU["sections"]))
        self.assertTrue(page.get_by_text("Début Double Stacked Cheddar Burger").is_visible())
        page.close()

    def test_section_navigation_works_without_horizontal_overflow_on_mobile(self):
        page = self.browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
        page.goto((ROOT / "dist" / "menu" / "index.html").as_uri())
        page.locator('a[href="#desserts"]').first.click()
        self.assertEqual(page.evaluate("location.hash"), "#desserts")
        self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 390)
        page.close()

    def test_each_item_has_a_lazy_loaded_visual_and_mobile_viewer(self):
        page = self.browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
        page.goto((ROOT / "dist" / "menu" / "index.html").as_uri())
        cards = page.locator(".menu-item")
        self.assertEqual(cards.count(), 92)
        self.assertEqual(cards.locator("img[loading='lazy']").count(), 92)
        cards.first.locator("button").click()
        self.assertTrue(page.get_by_role("dialog").is_visible())
        self.assertTrue(page.locator("#viewer-image").is_visible())
        self.assertFalse(page.locator("#viewer-model").is_visible())
        self.assertIn("DISH ILLUSTRATION", page.locator("#viewer-kind").inner_text())
        self.assertIn("Butter Chicken Poutine", page.get_by_role("dialog").inner_text())
        page.get_by_role("button", name="Next item").click()
        self.assertIn("Chicken Quesadilla", page.get_by_role("dialog").inner_text())
        page.keyboard.press("Escape")
        self.assertFalse(page.get_by_role("dialog").is_visible())
        page.close()

    def test_scan_code_points_to_public_menu(self):
        page = self.browser.new_page()
        page.goto((ROOT / "dist" / "menu" / "index.html").as_uri())
        qr = page.locator(".scan-code img")
        self.assertTrue(qr.is_visible())
        self.assertIn("github.io", page.locator(".scan-code a").get_attribute("href"))
        page.close()

    def test_real_model_metadata_activates_rotation_zoom_and_ar_viewer(self):
        page = self.browser.new_page(viewport={"width": 390, "height": 844})
        page.add_init_script("""(() => {
          customElements.define('model-viewer', class extends HTMLElement {});
          let menu;
          Object.defineProperty(window, 'DEBUT_MENU', {
            configurable: true,
            get() { return menu; },
            set(value) {
              value.sections[0].items[0].model = { glb: 'models/test-dish.glb', usdz: 'models/test-dish.usdz' };
              menu = value;
            },
          });
        })()""")
        page.goto((ROOT / "dist" / "menu" / "index.html").as_uri())
        page.locator(".menu-item button").first.click()
        model = page.locator("#viewer-model")
        self.assertTrue(model.is_visible())
        self.assertTrue(model.get_attribute("src").endswith("models/test-dish.glb"))
        self.assertTrue(model.get_attribute("ios-src").endswith("models/test-dish.usdz"))
        self.assertIsNotNone(model.get_attribute("camera-controls"))
        self.assertIsNotNone(model.get_attribute("ar"))
        self.assertFalse(page.locator("#viewer-image").is_visible())
        page.close()


if __name__ == "__main__":
    unittest.main()
