"""CRS 002 M2 — Bite 5: gr.Number sum calculator (04.pdf).

Two numeric inputs → one numeric output. Args order matches inputs list.

Run:
  . D:\\py_venv\\rag_application_builder_foundation\\set_env.ps1
  cd D:\\Workarea\\learning\\courses\\crs_002_build_rag_applications_get_started\\lab\\python
  python 13_m2_gradio_number_sum.py
"""

from __future__ import annotations

import gradio as gr


def add_numbers(num1: float, num2: float) -> float:
    return num1 + num2


def main() -> None:
    demo = gr.Interface(
        fn=add_numbers,
        inputs=[gr.Number(label="First number"), gr.Number(label="Second number")],
        outputs=gr.Number(label="Sum"),
        title="M2 — Sum calculator",
        description="04.pdf gradio_demo.py — gr.Number for in and out.",
        examples=[[3, 4], [10, 25], [-2, 7]],
    )
    demo.launch()


if __name__ == "__main__":
    main()