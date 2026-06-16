# Model Maps (Canonical Style)

When asked **"remember our model maps"** — these are the two reference bubble maps.

**Style ID:** `terraform_learnterraform_v1` (LearnTerraform TerraForm StudyBubble Style)

## Model Map 1 — Landscape

| | Path |
|---|------|
| **Open this** | `references/model_maps/landscape/iac_why_terraform_exists.html` |
| Topic JSON | `references/model_maps/landscape/iac_why_terraform_exists.studybubble.json` |
| Layout | `references/model_maps/landscape/iac_why_terraform_exists.layout.json` |
| Bubbles | 10 |

Use for: context, why, tool landscape, alternatives. Link out via `childTopics`.

## Model Map 2 — Workflow + cross-links

| | Path |
|---|------|
| **Open this** | `references/model_maps/workflow/terraform_core_workflow.html` |
| Topic JSON | `references/model_maps/workflow/terraform_core_workflow.studybubble.json` |
| Layout | `references/model_maps/workflow/terraform_core_workflow.layout.json` |
| Bubbles | 11 |

Use for: sequences, study paths, `mapResources`, navigation bubbles, `childTopics` to sibling maps.

## Rules (all new maps)

- Same viewer: search, filters, study paths, drag mode, **Export Layout**
- **8–15 bubbles** sweet spot, **20 max**
- Maps link to each other — never one crowded map

## Save layout (3 ways)

1. **Same browser** — drag bubbles; layout auto-saves. Reopen HTML → positions restored.
2. **Permanent in HTML** — after Export Layout, run from container `bubbles/` folder:
   ```powershell
   python ..\..\..\Study_bubbles\tools\studybubble.py import-layout "<exported>.layout.json"
   ```
   Or: `sync-layout` (scans your Downloads folder for `*.layout.json`)
3. **Manual** — **Import Layout** button in the map toolbar (loads a `.layout.json` file)

## Quick command

```powershell
cd Study_bubbles
python tools/studybubble.py model-maps
```

Registry: `references/model_maps/registry.json`