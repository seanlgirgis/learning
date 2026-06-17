"""Thin drill — imports the shared watson_llm helper."""

from watson_llm import llm_model

if __name__ == "__main__":
    response = llm_model(
        "Reply in one short sentence: what is prompt engineering?"
    )
    print(response)