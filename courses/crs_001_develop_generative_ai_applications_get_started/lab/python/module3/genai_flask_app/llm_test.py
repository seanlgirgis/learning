"""Lab sanity check — run all three models once."""

from model import granite_response, llama_response, mistral_response

SYSTEM = "You are an AI assistant helping with customer inquiries."
USER = "What is the capital of Canada? Also share one cool fact about it."


def call_all_models(system_prompt: str, user_prompt: str) -> None:
    for name, fn in (
        ("Llama", llama_response),
        ("Granite", granite_response),
        ("Mistral", mistral_response),
    ):
        print(f"\n=== {name} ===")
        result = fn(system_prompt, user_prompt)
        print(f"summary:   {result.get('summary', '')}")
        print(f"sentiment: {result.get('sentiment', '')}")
        print(f"response:  {result.get('response', '')}")


if __name__ == "__main__":
    call_all_models(SYSTEM, USER)