"""CRS 002 M2 — Bite 6: component zoo (04.pdf common_input_types.py).

Quiz prep: Slider, Dropdown, CheckboxGroup, Radio, Checkbox — one Interface.

Run:
  . D:\\py_venv\\rag_application_builder_foundation\\set_env.ps1
  cd D:\\Workarea\\learning\\courses\\crs_002_build_rag_applications_get_started\\lab\\python
  python 14_m2_gradio_components.py
"""

from __future__ import annotations

import gradio as gr


def sentence_builder(
    quantity: int,
    tech_worker_type: str,
    countries: list[str],
    place: str,
    activity_list: list[str],
    morning: bool,
) -> str:
    activities = " and ".join(activity_list) if activity_list else "worked"
    country_text = " and ".join(countries) if countries else "nowhere"
    when = "in the morning" if morning else "later in the day"
    return (
        f"The {quantity} {tech_worker_type}s from {country_text} "
        f"{activities} at the {place} {when}."
    )


def main() -> None:
    demo = gr.Interface(
        fn=sentence_builder,
        inputs=[
            gr.Slider(
                3,
                20,
                value=4,
                step=1,
                label="Count",
                info="Integer min/max/value/step → integer slider values",
            ),
            gr.Dropdown(
                ["Data Scientist", "Software Developer", "Software Engineer"],
                label="Role",
                info="Pick exactly one job title",
            ),
            gr.CheckboxGroup(
                ["Canada", "Japan", "France"],
                label="Countries",
                info="Pick multiple",
            ),
            gr.Radio(
                ["office", "restaurant", "meeting room"],
                label="Location",
                info="Radio forces one choice",
            ),
            gr.Dropdown(
                ["partied", "brainstormed", "coded", "fixed bugs"],
                value=["brainstormed"],
                multiselect=True,
                label="Activities",
                info="multiselect=True → many activities",
            ),
            gr.Checkbox(label="Morning", info="True / False only"),
        ],
        outputs="text",
        title="M2 — Gradio input types",
        description="04.pdf sentence_builder — study each widget before the quiz.",
        examples=[
            [3, "Software Developer", ["Canada", "Japan"], "restaurant", ["coded"], False],
            [4, "Data Scientist", ["Japan"], "office", ["brainstormed", "partied"], True],
            [10, "Software Engineer", ["Canada", "France"], "meeting room", ["brainstormed"], False],
            [8, "Data Scientist", ["France"], "restaurant", ["coded"], True],
        ],
    )
    demo.launch()


if __name__ == "__main__":
    main()