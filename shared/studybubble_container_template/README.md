# StudyBubble Container Template

Copy this folder as `<course_or_unit>/bubbles/` when adding bubble maps.

1. Replace `REPLACE_ME` and `REPLACE_TOPIC_ID` in `bubbles.ini`
2. Add `topics/<id>.studybubble.json` (see `planning/studybubble_map_standard.md`)
3. Build from the `bubbles/` folder:

```powershell
python ..\..\..\Study_bubbles\tools\studybubble.py build <topic_id>
```

4. Open `outputs/<topic_id>.html`

## Layout (built into engine — no extra setup)

| Step | What |
|------|------|
| Drag bubbles | Auto-saved in browser |
| Export Layout | Downloads `*.layout.json` |
| Permanent save | `python ..\..\..\Study_bubbles\tools\studybubble.py import-layout "...\Downloads\<id>.layout.json"` |

See `Study_bubbles/docs/LAYOUT_PERSISTENCE.md`.

Link the map from the unit/course `index.html`.