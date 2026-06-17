"""Minimal example: import llm_model from another playground file."""

from watson_llm import llm_model
if __name__ == "__main__":
    params = {
        "max_new_tokens": 512,
    }

    prompt = """When I was 6, my sister was half of my age. Now I am 70, what age is my sister?

                Provide three independent calculations and explanations, then determine the most consistent result.

    """
    response = llm_model(prompt, params)
    print(f"prompt: {prompt}\n")
    print(f"response :\n {response}\n")