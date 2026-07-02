# M2 — Gradio reading (`01.md`, `02.pdf`, `09.pdf`)

## Four setup steps (video + reading)

1. Write Python (`fn` — your logic)
2. Create `gr.Interface(fn=..., inputs=..., outputs=...)`
3. `demo.launch()` — local web server (default port **7860**)
4. Open the URL; optional `share=True` for a temporary public link

## `gr.Interface` — three core arguments

| Arg | Job |
|-----|-----|
| `fn` | Python function to wrap |
| `inputs` | One component **per** function parameter (order matters) |
| `outputs` | One component **per** return value (or one component for a single return) |

Multiple inputs → pass a **list**: `[gr.Textbox(), gr.Number()]`

Shorthand strings work: `inputs=["text", "slider"]`, `outputs=["text"]`

Gradio has **30+** built-in components (`Textbox`, `Image`, `HTML`, …).

## First demo — greet + slider (`02.pdf`)

```python
def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)
```

- `int(intensity)` — slider may return float; cast when you need whole repeats
- **Integer slider rule** (`09.pdf`): if **min, max, value, and step** are all integers → slider values are integers

## Components you already touch in M2

| Component | Use |
|-----------|-----|
| `gr.Textbox` | Text in / text out |
| `gr.Number` | Numeric in / out (sum calculator lab) |
| `gr.File` | Upload; backend gets **file path(s)** |
| `gr.Slider` | Pick number in range |

## Outputs beyond text

| Component | Use |
|-----------|-----|
| `gr.Label` | Classification — class names + probabilities; `num_top_classes=3` limits rows |
| `"text"` | Same idea as `gr.Textbox()` for output |

## `examples=` on Interface

List of lists — each inner list is one prefilled row in the Examples table.

## Local scripts

| # | Script |
|---|--------|
| 09 | Echo — one `Textbox` in, one out |
| 12 | Greet + `Slider` — Interface 3-arg pattern |