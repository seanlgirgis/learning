# StudyBubble Map Standard (Canonical)

**Model maps (canonical copies in learning repo):**

See `Study_bubbles/MODEL_MAPS.md` — command: `python tools/studybubble.py model-maps`

| Type | HTML | Bubbles |
|------|------|---------|
| Landscape | `Study_bubbles/references/model_maps/landscape/iac_why_terraform_exists.html` | 10 |
| Workflow + links | `Study_bubbles/references/model_maps/workflow/terraform_core_workflow.html` | 11 |

## Two map types

**1. Landscape** (`iac_why_terraform_exists`) — why/context map  
- Concept groups (4–6 groups)  
- Bubbles explain a domain landscape  
- `childTopics` on key bubbles → other maps  

**2. Workflow / deep** (`terraform_core_workflow`) — how/sequence map  
- Workflow groups + optional **Map Navigation** group  
- `paths` = clickable study lanes  
- `mapResources` = course home, related maps (not on random bubbles)  
- `childTopics` + `externalLinks` on specific bubbles  
- Navigation bubbles link to sibling maps  

## Size rule

| Rule | Value |
|------|-------|
| **Hard max** | 20 bubbles — validator fails above this |
| **Sweet spot** | 8–15 (TerraForm uses 10–11) |
| **Too big?** | Split into a second map; link with `childTopics` |

## Cross-map linking

```json
"childTopics": [
  { "label": "Terraform 1000-Foot View", "topic": "terraform_1000_foot_view.studybubble.json" }
]
```

- Maps link **to each other** via `childTopics` → opens sibling `.html` in `outputs/`  
- `mapResources` for map-level links (tutorials, course home, related maps)  
- `externalLinks` for study pages, docs (new tab)  

## Per course/unit layout

```text
<unit_or_course>/bubbles/
  bubbles.ini
  topics/*.studybubble.json
  layouts/*.layout.json    ← saved after Export Layout + sync
  outputs/*.html           ← generated; open in browser
  assets/
```

Engine: `D:\Workarea\learning\Study_bubbles`  
Template: `shared/studybubble_container_template/`

## Build workflow

```powershell
cd <container>/bubbles
python ..\..\Study_bubbles\tools\studybubble.py build <topic_id>
# After drag + Export Layout:
python ..\..\Study_bubbles\tools\studybubble.py sync-layout
```

## Features (all maps)

Search, group filters, study paths, drag mode, **Export Layout**, parent/child nav, resizable side panel — same as TerraForm outputs.