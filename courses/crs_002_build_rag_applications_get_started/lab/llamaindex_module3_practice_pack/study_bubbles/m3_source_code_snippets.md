# Module 3 Source Code Snippets

Big idea:

```text
Source type → Loader / reader / wrapper → list[Document]
```

## Basic folder load

```python
from pathlib import Path
from llama_index.core import SimpleDirectoryReader

DATA_DIR = Path("data/company_knowledge")
documents = SimpleDirectoryReader(str(DATA_DIR)).load_data()
```

## Recursive folder load

```python
documents = SimpleDirectoryReader(
    "data/company_knowledge",
    recursive=True
).load_data()
```

## Filter by extension

```python
documents = SimpleDirectoryReader(
    "data/company_knowledge",
    required_exts=[".md", ".csv"]
).load_data()
```

## Exclude files

```python
documents = SimpleDirectoryReader(
    "data/company_knowledge",
    exclude=["*/archive/*", "*.tmp"]
).load_data()
```

## Single file / selected files

```python
from pathlib import Path
from llama_index.core import SimpleDirectoryReader

file_path = Path("data/company_knowledge/01_company_overview.md")

documents = SimpleDirectoryReader(
    input_files=[str(file_path)]
).load_data()
```

## Manual in-memory text

```python
from llama_index.core import Document

documents = [
    Document(
        text="Refund policy: customers may request refunds within 30 days.",
        metadata={"source_type": "manual_text", "topic": "refund_policy"}
    )
]
```

## Web page

```python
# pip install llama-index-readers-web
from llama_index.readers.web import SimpleWebPageReader

documents = SimpleWebPageReader(
    html_to_text=True
).load_data(["https://example.com"])
```

## API JSON

```python
import json
import requests
from llama_index.core import Document

response = requests.get("https://api.example.com/profile/123", timeout=20)
response.raise_for_status()
data = response.json()

documents = [
    Document(
        text=json.dumps(data, indent=2),
        metadata={"source_type": "api", "endpoint": "profile/123"}
    )
]
```

## Database rows

```python
import sqlite3
from llama_index.core import Document

conn = sqlite3.connect("company.db")
rows = conn.execute("select id, title, body from policies").fetchall()

documents = [
    Document(
        text=f"Title: {title}\n\n{body}",
        metadata={"source_type": "database", "table": "policies", "row_id": row_id}
    )
    for row_id, title, body in rows
]
```

## Cloud storage

```python
from llama_index.core import SimpleDirectoryReader

# Download cloud files to a local cache folder first.
documents = SimpleDirectoryReader(
    "local_cache/cloud_docs",
    recursive=True
).load_data()
```

Rule:

```text
Source = where knowledge lives
Loader = code that reads source
Document = loaded text + metadata
```
