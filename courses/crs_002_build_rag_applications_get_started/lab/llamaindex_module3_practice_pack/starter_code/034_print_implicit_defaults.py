from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter


def main() -> None:
    print("CURRENT LLAMAINDEX DEFAULTS / SETTINGS")
    print("=" * 80)

    print("\nSettings.text_splitter:")
    print(Settings.text_splitter)
    print("Type:", type(Settings.text_splitter))

    splitter = Settings.text_splitter

    print("\nPossible splitter attributes:")
    for name in [
        "chunk_size",
        "chunk_overlap",
        "separator",
        "paragraph_separator",
        "secondary_chunking_regex",
    ]:
        if hasattr(splitter, name):
            print(f"{name}: {getattr(splitter, name)}")

    print("\nFresh SentenceSplitter() defaults:")
    fresh = SentenceSplitter()
    print(fresh)
    print("Type:", type(fresh))

    for name in [
        "chunk_size",
        "chunk_overlap",
        "separator",
        "paragraph_separator",
        "secondary_chunking_regex",
    ]:
        if hasattr(fresh, name):
            print(f"{name}: {getattr(fresh, name)}")


if __name__ == "__main__":
    main()