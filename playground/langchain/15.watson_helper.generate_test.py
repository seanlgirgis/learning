"""Lab 15 — test watson_helper (ModelInference from WATSONX_* env).

Like the LangChain notebook LOCAL SETUP + model.generate() demo.

Run:
    D:\\py_venv\\rag_application_builder_foundation\\set_env.ps1
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\15.watson_helper.generate_test.py
"""

from watson_helper import credentials, model, model_id


def main() -> None:
    print("Loaded watson_helper.py")
    print("Model:", model_id)
    print("URL:", credentials["url"])
    print()

    prompt = "In today's sales meeting, we "
    print("Prompt:", repr(prompt))
    msg = model.generate(prompt)
    print(msg["results"][0]["generated_text"])


if __name__ == "__main__":
    main()