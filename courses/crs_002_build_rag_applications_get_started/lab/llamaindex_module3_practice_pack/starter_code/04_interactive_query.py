from pathlib import Path
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "company_knowledge"

def main() -> None:
    documents = SimpleDirectoryReader(str(DATA_DIR)).load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

    print("Ask questions about the company knowledge base.")
    print("Type 'exit' or 'quit' to stop.")
    print()

    while True:
        question = input("Question> ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue

        response = query_engine.query(question)
        print()
        print(response)
        print()

if __name__ == "__main__":
    main()
