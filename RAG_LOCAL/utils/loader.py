from __future__ import annotations

from pathlib import Path


def load_documents(path):
    from langchain_community.document_loaders import PyPDFDirectoryLoader

    docs_path = Path(path)
    if not docs_path.exists():
        raise FileNotFoundError(f"Document directory does not exist: {docs_path}")

    if not any(docs_path.glob("*.pdf")):
        raise FileNotFoundError(f"No PDF files found in: {docs_path}")

    loader = PyPDFDirectoryLoader(str(docs_path))
    return loader.load()
