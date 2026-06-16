# Layout Persistence (Engine Default)

Every bubble map built from this engine gets layout persistence automatically.

## What happens now (built into viewer + CLI)

| Action | Result |
|--------|--------|
| Drag a bubble | Layout saved in browser `localStorage` |
| Reopen same HTML (same browser) | Positions restored |
| **Export Layout** | Downloads `.layout.json` **and** saves in browser |
| **Import Layout** | Loads a `.layout.json` file immediately |
| `import-layout <file>` | Copies layout into `layouts/` and rebuilds HTML with positions baked in |
| `sync-layout` | Imports all `*.layout.json` from Downloads, then rebuilds |

## Permanent layout (recommended after export)

From a container folder (`bubbles/` with `bubbles.ini`):

```powershell
python ..\..\..\Study_bubbles\tools\studybubble.py import-layout "<exported>.layout.json"
```

(`sync-layout` scans your Downloads folder automatically — no path needed.)

Rebuild embeds `x`/`y` on each node in the single-file HTML.

## New container checklist

1. Copy `shared/studybubble_container_template/` → `<unit>/bubbles/`
2. Add `topics/<id>.studybubble.json`
3. `python .../studybubble.py build <id>`
4. Open `outputs/<id>.html` — drag, export, import-layout as needed
5. Keep `layouts/<id>.layout.json` in git when positions are final

## Engine files (do not fork per map)

- `viewer/bubble_viewer.js` — localStorage + import/export UI
- `viewer/bubble_viewer.html` — toolbar buttons
- `src/study_bubbles/build_topic.py` — applies `layouts/*.layout.json` on build
- `tools/studybubble.py` — `build`, `import-layout`, `sync-layout`