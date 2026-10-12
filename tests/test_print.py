import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import zxingcpp
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "DEBUT-3D-Menu-Print.pdf"


class PrintMenuTests(unittest.TestCase):
    def test_pdf_has_cover_and_full_menu(self):
        self.assertTrue(PDF.exists())
        info = subprocess.check_output(["pdfinfo", str(PDF)], text=True)
        pages = int(next(line.split(":", 1)[1] for line in info.splitlines() if line.startswith("Pages:")))
        self.assertGreaterEqual(pages, 4)
        text = subprocess.check_output(["pdftotext", str(PDF), "-"], text=True)
        normalized = text.casefold()
        for name in ("DÉBUT", "Appetizers", "Début Double Stacked Cheddar Burger", "Butter Chicken", "Ras Malai", "Deals & Promos"):
            self.assertIn(name.casefold(), normalized)

    def test_cover_qr_opens_public_phone_menu(self):
        with TemporaryDirectory() as directory:
            prefix = str(Path(directory) / "cover")
            subprocess.check_call(["pdftoppm", "-f", "1", "-l", "1", "-scale-to", "1800", "-png", str(PDF), prefix], stdout=subprocess.DEVNULL)
            image = Image.open(prefix + "-1.png")
            codes = zxingcpp.read_barcodes(image)
            self.assertIn("https://benzom666.github.io/debut-3d-menu-temp/menu/#appetizers", [code.text for code in codes])


if __name__ == "__main__":
    unittest.main()
