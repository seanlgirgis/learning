"""Examples that call the shared watson_llm helper."""

import sys

from watson_llm import GenParams, llm_model


def run_few_prompts():
    params = {
        "max_new_tokens": 128,
        "min_new_tokens": 10,
        "temperature": 0.5,
        "top_p": 0.2,
        "top_k": 1,
    }
    prompts = [
        "What is the capital of France?",
        "Write a haiku about the ocean.",
        "Summarize the plot of Romeo and Juliet in one sentence.",
    ]
    for prompt in prompts:
        print(f"Prompt: {prompt}")
        print(f"Response: {llm_model(prompt, params)}")
        print("-" * 80)


def zero_shot_example():
    prompt = """Classify the following statement as true or false: 
            'The Eiffel Tower is located in Berlin.'

            Answer:
    """
    response = llm_model(prompt)
    print(f"Prompt: {prompt}\nResponse: {response}")


def few_zero_shots():
    movie_review_prompt = """
                Classify the following movie as great or rotten_tomatoe: 
                'AS Good AS It Gets'
    """

    climate_change_prompt = """
                Classify statement as Truth or Fake: 
                'Man Made Climate Change'
    """

    translation_prompt = (
        "Translate the following English sentence to Spanish. "
        "Reply with only the Spanish translation.\n\n"
        "English: Soccer is the most popular sport\n"
        "Spanish:"
    )
    responses = {
        "movie_review": llm_model(movie_review_prompt),
        "climate_change": llm_model(climate_change_prompt),
        "translation": llm_model(translation_prompt),
    }

    for prompt_type, response in responses.items():
        print(f"=== {prompt_type.upper()} RESPONSE ===")
        print(response)
        print()


def one_shot_example():
    params = {
        GenParams.MAX_NEW_TOKENS: 80,
        GenParams.TEMPERATURE: 0.1,
        GenParams.MIN_NEW_TOKENS: 5,
    }

    prompt = (
        "Here is an example of translating a sentence from English to French:\n\n"
        'English: "How is the weather today?"\n'
        'French: "Comment est le temps aujourd\'hui?"\n\n'
        "Now, translate the following sentence from English to French.\n"
        "Reply with only the French translation on one line.\n\n"
        'English: "Soccer is the most popular sport in the world"\n'
        "French:"
    )

    response = llm_model(prompt, params)
    print(f"Prompt:\n{prompt}\n\nResponse: {response.strip()}")


if __name__ == "__main__":
    one_shot_example()

    sys.exit(0)
    print("-" * 50, "Capital of France Concisely", "-" * 50)
    print(
        llm_model(
            "Please respond concisely just for the question given. "
            "What is the capital of France?"
        )
    )
    print("-" * 50, "wind example with no context", "-" * 50)
    params = {
        "max_new_tokens": 128,
        "min_new_tokens": 10,
        "temperature": 0.5,
        "top_p": 0.2,
        "top_k": 1,
    }

    prompt = "The wind is "
    response = llm_model(prompt, params)
    print(f"prompt: {prompt}\n")
    print(f"response : {response}\n")

    print("-" * 50, "few prompts with no context", "-" * 50)
    run_few_prompts()

    print("\n", "-" * 50, "zero shot example", "-" * 50)
    zero_shot_example()

    print("\n", "-" * 50, "few zero shot examples", "-" * 50)
    few_zero_shots()