from pathlib import Path
from llama_index.core import SimpleDirectoryReader

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "company_knowledge"

def main() -> None:
    documents = SimpleDirectoryReader(str(DATA_DIR)).load_data()

    print(f"Loaded documents: {len(documents)}")
    print()

    for i, doc in enumerate(documents, start=1):
        for key, val in doc.metadata.items():
            print(f"   {key}: {val}")

        source = doc.metadata.get("file_name") or doc.metadata.get("file_path") or "unknown"
        preview = doc.text[:220].replace("\n", " ")
        print(f"{i}. Source: {source}")
        print(f"   Preview: {preview}...")
        print()

if __name__ == "__main__":
    main()
