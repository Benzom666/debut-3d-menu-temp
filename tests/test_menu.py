import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MenuContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.menu = json.loads((ROOT / "menu.json").read_text())

    def test_core_sections_are_present(self):
        titles = {section["title"] for section in self.menu["sections"]}
        self.assertTrue({"Appetizers", "Salads & Bowls", "Hand-helds", "Grills & Mains", "Flavours from the East", "Pasta", "Soups", "Desserts", "Beverages", "Deals & Promos"}.issubset(titles))

    def test_representative_prices_match_source(self):
        items = {item["name"]: item for section in self.menu["sections"] for item in section["items"]}
        self.assertEqual(items["Début Double Stacked Cheddar Burger"]["price"], 23)
        self.assertEqual(items["Butter Chicken"]["price"], 22)
        self.assertEqual(items["New York Steak with Mushroom Sauce"]["price"], 33.5)
        self.assertEqual(items["Ras Malai"]["price"], 14)

    def test_item_names_are_unique_and_pricing_is_numeric_when_present(self):
        items = [item for section in self.menu["sections"] for item in section["items"]]
        names = [item["name"] for item in items]
        self.assertEqual(len(names), len(set(names)))
        for item in items:
            if "price" in item:
                self.assertIsInstance(item["price"], (int, float))

    def test_unpriced_soft_drinks_remain_unpriced(self):
        items = {item["name"]: item for section in self.menu["sections"] for item in section["items"]}
        for name in ("Water", "Pop", "Juice"):
            self.assertNotIn("price", items[name])

    def test_browser_data_matches_source(self):
        generated = (ROOT / "dist" / "menu-data.js").read_text()
        self.assertTrue(generated.startswith("window.DEBUT_MENU = "))
        browser_data = json.loads(generated.removeprefix("window.DEBUT_MENU = ").removesuffix(";\n"))
        self.assertEqual(browser_data, self.menu)


if __name__ == "__main__":
    unittest.main()
