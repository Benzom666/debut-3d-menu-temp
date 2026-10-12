"""Validate the editable menu source and write the browser data bundle."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    menu = json.loads((ROOT / "menu.json").read_text(encoding="utf-8"))
    if not menu.get("sections"):
        raise ValueError("Menu needs at least one section")
    ids = [section["id"] for section in menu["sections"]]
    if len(ids) != len(set(ids)):
        raise ValueError("Section IDs must be unique")
    for section in menu["sections"]:
        if not section.get("items"):
            raise ValueError(f"Empty menu section: {section['id']}")
        for item in section["items"]:
            if not item.get("name"):
                raise ValueError(f"Unnamed item in {section['id']}")
            if not item.get("description"):
                raise ValueError(f"Missing description for {item['name']} in {section['id']}")
    output = ROOT / "dist" / "menu-data.js"
    output.write_text("window.DEBUT_MENU = " + json.dumps(menu, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    print(f"Wrote {output} ({sum(len(s['items']) for s in menu['sections'])} items)")


if __name__ == "__main__":
    main()
