from llama_index.core import Settings


def main() -> None:
    print("LLM CONFIG")
    print("=" * 80)

    print("\nSettings.llm:")
    print(Settings.llm)
    print("Type:", type(Settings.llm))

    print("\nSettings.embed_model:")
    print(Settings.embed_model)
    print("Type:", type(Settings.embed_model))


if __name__ == "__main__":
    main()