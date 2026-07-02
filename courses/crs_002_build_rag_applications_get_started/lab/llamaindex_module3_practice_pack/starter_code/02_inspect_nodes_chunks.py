from pathlib import Path
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "company_knowledge"

def main() -> None:
    documents = SimpleDirectoryReader(str(DATA_DIR)).load_data()

    splitter = SentenceSplitter(
        chunk_size=512,
        chunk_overlap=50,
    )

    nodes = splitter.get_nodes_from_documents(documents)

    print("Document count:", len(documents))
    print("Node count:", len(nodes))
    print()

    node = nodes[0]

    print("FIRST NODE TYPE:")
    print(type(node))
    print()

    print("FIRST NODE TEXT PREVIEW:")
    print(node.get_content()[:500])
    print()

    print("FIRST NODE METADATA:")
    print(node.metadata)

if __name__ == "__main__":
    main()