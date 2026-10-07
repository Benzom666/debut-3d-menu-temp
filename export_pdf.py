"""Export the print menu from the same HTML used by the digital menu."""

from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "DEBUT-3D-Menu-Print.pdf"


def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto((ROOT / "dist" / "index.html").as_uri(), wait_until="load")
        page.emulate_media(media="print")
        page.pdf(path=str(OUTPUT), format="Letter", print_background=True, prefer_css_page_size=True)
        browser.close()
    (ROOT / "dist" / OUTPUT.name).write_bytes(OUTPUT.read_bytes())
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
