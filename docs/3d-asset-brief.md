# Début dish models

The menu has 92 illustrated items. A single illustration cannot reveal the unseen sides of a dish. To give guests a truthful 360° view, each item needs an actual textured 3D mesh created from a multi-angle capture or a carefully modeled source.

## Deliverables per item

- A web-ready `.glb` with real geometry and baked textures. Set the physical scale so AR shows a believable serving size.
- An optional `.usdz` for iOS Quick Look. The viewer can also generate USDZ from the GLB on supported devices, but a reviewed USDZ is preferable for quality control.
- A still poster image for the loading state, ideally from the final model and matching the real presentation.
- Restaurant approval that the model resembles the served dish, plus rights to publish the assets.

Place approved files in `dist/models/` and add an optional `model` object to the matching item in `menu.json`:

```json
"model": {
  "glb": "models/appetizers-01.glb",
  "usdz": "models/appetizers-01.usdz"
}
```

`python3 build.py` rejects missing files and paths outside `dist/models/`. On desktop, guests can drag to rotate and scroll to zoom. On phones, they can use touch and, where supported, open AR through [model-viewer](https://modelviewer.dev/docs/). Desktop AR depends on compatible WebXR hardware; the 360° viewer itself works on desktop. Items without approved models keep the illustrated image viewer.

Before rollout, inspect every model at desktop and phone widths, test AR on real iOS and Android devices, and compare the geometry, texture, and portion size with the actual dish. Keep the existing QR pointed at the public `/menu/` page; it will pick up approved models as they are added.
