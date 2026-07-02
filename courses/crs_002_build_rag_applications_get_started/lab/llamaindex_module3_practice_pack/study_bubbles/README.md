# Module 3 StudyBubble maps

Uses the **real** `Study_bubbles` engine (same as CRS 001): search, drag mode, export/import layout, study paths, side panel details.

## Open maps

```powershell
start D:\Workarea\learning\courses\crs_002_build_rag_applications_get_started\lab\llamaindex_module3_practice_pack\study_bubbles\index.html
```

**Start map:** `outputs/m3_rag_pipeline.html`

## Rebuild after editing JSON

From this folder:

```powershell
cd D:\Workarea\learning\courses\crs_002_build_rag_applications_get_started\lab\llamaindex_module3_practice_pack\study_bubbles
python D:\Workarea\learning\Study_bubbles\tools\studybubble.py build m3_rag_pipeline
python D:\Workarea\learning\Study_bubbles\tools\studybubble.py build m3_source
python D:\Workarea\learning\Study_bubbles\tools\studybubble.py build m3_loader
```

Or rebuild one topic: `studybubble.py build <topic_id>`

## Edit content

| What | Where |
|------|--------|
| Bubble text, code notes, links | `topics/*.studybubble.json` |
| Bubble positions (after drag) | Export layout in browser → `studybubble.py import-layout file.layout.json` |
| Saved positions | `layouts/<topic_id>.layout.json` |

## Phase 1 (built)

- `m3_rag_pipeline` — main map
- `m3_source`, `m3_loader`, `m3_loader_sources` — detail maps

Scaffolds: `m3_documents` through `m3_answer` — upgrade JSON as we study.

## Not the custom static version

Earlier prototype HTML is in `archive/custom_static_html/` — it did **not** use StudyBubble viewer features.