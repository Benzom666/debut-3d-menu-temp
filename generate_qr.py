"""Generate the high-resolution scan code for the temporary public menu URL."""

from pathlib import Path
import qrcode
from qrcode.constants import ERROR_CORRECT_H

ROOT = Path(__file__).resolve().parent
TARGET = "https://benzom666.github.io/debut-3d-menu-temp/#appetizers"


def main():
    qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_H, box_size=16, border=4)
    qr.add_data(TARGET)
    qr.make(fit=True)
    image = qr.make_image(fill_color="#171815", back_color="#ffffff")
    output = ROOT / "dist" / "scan-menu-qr.png"
    image.save(output)
    print(f"Wrote {output} for {TARGET}")


if __name__ == "__main__":
    main()
