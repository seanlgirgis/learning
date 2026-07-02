from pathlib import Path
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "company_knowledge"

def main() -> None:
    documents = SimpleDirectoryReader(str(DATA_DIR)).load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

    questions = [
        "What is the support escalation rule for Sev-1 incidents?",
        "Which product is better for dashboard-style reports?",
        "What changed after the May 2026 analytics outage?",
        "Can I upload API keys into an AI tool?",
        "Who is the CEO of Northwind Analytics?",
    ]

    for question in questions:
        print("=" * 80)
        print(f"QUESTION: {question}")
        response = query_engine.query(question)
        print()
        print("ANSWER:")
        print(response)
        print()

if __name__ == "__main__":
    main()
