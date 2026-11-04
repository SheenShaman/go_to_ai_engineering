from pathlib import Path

from src.app.rag.embeddings import ingest_document

project_root = Path(__file__).resolve().parents[1]
file_path = project_root / "data" / "sample_docs" / "postgres_indexes.md"

print(ingest_document(file_path))
