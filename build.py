"""Validate the editable menu source and write the browser data bundle."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def validate_model(model, item_name):
    if not isinstance(model, dict) or not isinstance(model.get("glb"), str):
        raise ValueError(f"Invalid model metadata for {item_name}")
    for key, suffix in (("glb", ".glb"), ("usdz", ".usdz")):
        value = model.get(key)
        if value is None:
            continue
        if not isinstance(value, str):
            raise ValueError(f"Invalid {key} path for {item_name}")
        path = Path(value)
        if path.is_absolute() or path.parts[:1] != ("models",) or ".." in path.parts or path.suffix.lower() != suffix:
            raise ValueError(f"Unsafe {key} path for {item_name}: {value}")
        if not (ROOT / "dist" / path).is_file():
            raise ValueError(f"Missing {key} file for {item_name}: {value}")


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
            if "model" in item:
                validate_model(item["model"], item["name"])
    output = ROOT / "dist" / "menu-data.js"
    output.write_text("window.DEBUT_MENU = " + json.dumps(menu, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    print(f"Wrote {output} ({sum(len(s['items']) for s in menu['sections'])} items)")


if __name__ == "__main__":
    main()
