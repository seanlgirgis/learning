"""Minimal example: import llm_model from another playground file."""

from watson_llm import llm_model
if __name__ == "__main__":
# 1. Prompt for decision-making process
    decision_making_prompt = """
    Consider this situation: A student is trying to decide whether to study tonight or go to a movie with friends. They have a test in two days.

    Think through this decision step-by-step, considering the pros and cons of each option, and what factors might be most important in making this choice.
    """

    # 2. Prompt for explaining a process
    sandwich_making_prompt = """
    Explain how to make a peanut butter and jelly sandwich.

    Break down each step of the process in detail, from gathering ingredients to finishing the sandwich.
    """

    responses = {}
    responses["decision_making"] = llm_model(decision_making_prompt)
    responses["sandwich_making"] = llm_model(sandwich_making_prompt)

    for prompt_type, response in responses.items():
        print(f"=== {prompt_type.upper()} RESPONSE ===")
        print(response)
        print()    