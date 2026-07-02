from pathlib import Path
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "company_knowledge"

def main() -> None:
    documents = SimpleDirectoryReader(str(DATA_DIR)).load_data()

    transformations = [
        SentenceSplitter(
            chunk_size=512,
            chunk_overlap=50,
        )
    ]

    index = VectorStoreIndex.from_documents(
        documents,
        transformations=transformations,
    )

    query_engine = index.as_query_engine()

    response = query_engine.query("What is the support escalation rule for Sev-1 incidents?")
    print(response)

if __name__ == "__main__":
    main()