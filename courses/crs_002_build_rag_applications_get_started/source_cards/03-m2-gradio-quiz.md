# M2 — Gradio quiz drill

Format: question → **answer** (from `04.pdf`, `09.pdf`, `01.md`)

---

- File uploads in Gradio? → **gr.File**
- Text + numeric inputs together? → **list of gr.Textbox and gr.Number** (order matches `fn` args)
- Role of `gr.Interface`? → **specifies inputs/outputs (and fn) for Python functions**
- Slider returns integers when? → **min, max, value, and step are all integers**
- User must pick **exactly one** of three options? → **Dropdown** (single select) or **Radio** — not Checkbox, not CheckboxGroup, not Textbox
- Pick **multiple** from a list? → **CheckboxGroup** (or Dropdown with `multiselect=True`)
- Single true/false? → **Checkbox**
- Classification probabilities in UI? → **gr.Label** (often `num_top_classes=N`)
- Share app publicly from laptop? → **`launch(share=True)`**
- Default local port? → **7860**
- `fn` has 2 parameters; Interface needs → **2 input components in order**
- Gradio needs JavaScript/CSS skills? → **No** (per reading)
- `examples=` on Interface? → **list of lists** — each inner list = one example row

---

## Mnemonics

- **Interface trio:** `fn` · `inputs` · `outputs`
- **One-of-three:** Dropdown or Radio
- **Many-of-list:** CheckboxGroup
- **Integer slider:** min + max + value + step all int