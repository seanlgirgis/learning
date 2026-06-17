"""Minimal example: import llm_model from another playground file."""

from watson_llm import llm_model
if __name__ == "__main__":
    params = {
    "max_new_tokens": 512,
    "temperature": 0.5,
    }

    prompt = """Consider the problem: 'A store had 22 apples. They sold 15 apples today and got a new delivery of 8 apples. 
                How many apples are there now?’

                Break down each step of your calculation

    """
    response = llm_model(prompt, params)
    print(f"prompt: {prompt}\n")
    print(f"response : {response}\n")