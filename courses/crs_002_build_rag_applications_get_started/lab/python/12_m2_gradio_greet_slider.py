"""CRS 002 M2 — Bite 4: greet + slider (02.pdf first demo).

Shows Interface's three core args and string shortcuts for components.

Run:
  . D:\\py_venv\\rag_application_builder_foundation\\set_env.ps1
  cd D:\\Workarea\\learning\\courses\\crs_002_build_rag_applications_get_started\\lab\\python
  python 12_m2_gradio_greet_slider.py
"""

from __future__ import annotations

import gradio as gr


def greet(name: str, intensity: float) -> str:
    """Course pattern: slider value may be float — cast with int() for repeats."""
    who = (name or "").strip() or "friend"
    return "Hello, " + who + "!" * int(intensity)


def main() -> None:
    demo = gr.Interface(
        fn=greet,
        inputs=[
            gr.Textbox(label="Name"),
            gr.Slider(1, 10, value=3, step=1, label="Intensity"),
        ],
        outputs=gr.Textbox(label="Greeting"),
        title="M2 — Greet + slider",
        description=(
            "Quiz rule: min, max, value, and step all integers → integer slider. "
            "Still use int() in fn as a safety cast."
        ),
    )
    demo.launch()


if __name__ == "__main__":
    main()