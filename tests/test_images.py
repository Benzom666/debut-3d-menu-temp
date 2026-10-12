import json
import unittest
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


class ImageCoverageTests(unittest.TestCase):
    def test_each_menu_entry_has_a_web_image(self):
        menu = json.loads((ROOT / "menu.json").read_text())
        missing = []
        for section in menu["sections"]:
            for index, _item in enumerate(section["items"], 1):
                path = ROOT / "dist" / "images" / f"{section['id']}-{index:02d}.webp"
                if not path.exists() or path.stat().st_size < 1000:
                    missing.append(path.name)
        self.assertEqual(missing, [])

    def test_generated_images_cover_every_menu_entry(self):
        menu = json.loads((ROOT / "menu.json").read_text())
        expected = {
            f"{section['id']}-{index:02d}"
            for section in menu["sections"]
            for index, _item in enumerate(section["items"], 1)
        }
        generated = ROOT / "dist" / "images" / "generated"
        originals = ROOT / "assets" / "generated-originals"
        self.assertEqual({path.stem for path in generated.glob("*.webp")}, expected)
        self.assertEqual({path.stem for path in originals.glob("*.png")}, expected)
        for path in generated.glob("*.webp"):
            with Image.open(path) as image:
                self.assertEqual(image.mode, "RGBA", path.name)
                self.assertLessEqual(image.getpixel((0, 0))[3], 1, path.name)

    def test_images_are_large_transparent_renders(self):
        for path in (ROOT / "dist" / "images").glob("*.webp"):
            with Image.open(path) as image:
                self.assertGreaterEqual(image.width, 500, path.name)
                self.assertIn(image.mode, ("RGBA", "LA"), path.name)
                self.assertLess(image.getchannel("A").getextrema()[0], 50, path.name)


if __name__ == "__main__":
    unittest.main()
