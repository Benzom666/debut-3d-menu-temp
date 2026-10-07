import subprocess
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
