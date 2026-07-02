# M2 — Simple Gradio lab (`04.pdf`)

## Lab arc

1. **Sum calculator** — `gr.Number()` × 2 → `gr.Number()` out
2. **Sentence builder** — all common input types on one screen
3. **Terminal LLM** — `watsonx_llm.invoke(query)` (Skills Network)
4. **Gradio LLM chat** — same model, `gr.Textbox` in/out

## `gr.Number`

Creates a numeric field for input **or** output. Function receives real numbers; return a number for numeric output.

## Common inputs (quiz vocabulary)

| Component | Behavior |
|-----------|----------|
| **Checkbox** | Single **True / False** |
| **CheckboxGroup** | **Multiple** choices from a list |
| **Dropdown** | **One** choice by default; `multiselect=True` → many |
| **Radio** | **Exactly one** choice (forced) |
| **File** | Upload file(s) |
| **Image** | Upload / select image |
| **Slider** | Value between min and max; `step` = increment |
| **Textbox** | Free text |

### Pick the right widget

| Need | Use |
|------|-----|
| Yes/no flag | `Checkbox` |
| Pick several countries | `CheckboxGroup` |
| Pick **one** role from three | `Dropdown` **or** `Radio` |
| Pick a number 3–20 | `Slider` |
| Type a question | `Textbox` |
| Upload PDF | `File` |

## Sentence builder (`common_input_types.py` in lab)

Function args map 1:1 to inputs list:

1. `gr.Slider(3, 20, value=4, step=1, ...)` → quantity
2. `gr.Dropdown([...])` → job title (one of three)
3. `gr.CheckboxGroup([...])` → countries (many)
4. `gr.Radio([...])` → place (one)
5. `gr.Dropdown(..., multiselect=True)` → activities (many)
6. `gr.Checkbox` → morning True/False

## LLM + Gradio (`llm_chat.py` pattern)

```text
initialize LLM once → generate_response(prompt) → gr.Interface(fn=..., inputs=Textbox, outputs=Textbox)
```

Course knobs: `MAX_NEW_TOKENS`, `TEMPERATURE`, `allow_flagging="never"`

## Local scripts

| # | Script |
|---|--------|
| 13 | Two `Number` fields — add |
| 14 | Full component zoo (sentence builder) |
| 15 | LLM chat in browser (no RAG) |