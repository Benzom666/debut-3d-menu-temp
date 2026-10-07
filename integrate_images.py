"""Convert generated transparent PNG assets into compact web images."""

import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "image_sources.json"
OUTPUT = ROOT / "dist" / "images"


def main():
    sources = json.loads(SOURCES.read_text(encoding="utf-8"))
    OUTPUT.mkdir(exist_ok=True)
    for item_id, source in sources.items():
        target = OUTPUT / f"{item_id}.webp"
        if target.exists() and target.stat().st_mtime >= Path(source).stat().st_mtime:
            continue
        with Image.open(source) as image:
            image = image.convert("RGBA")
            image.thumbnail((768, 768), Image.Resampling.LANCZOS)
            image.save(target, "WEBP", quality=84, method=4)
    print(f"Integrated {len(sources)} menu images into {OUTPUT}")


if __name__ == "__main__":
    main()
