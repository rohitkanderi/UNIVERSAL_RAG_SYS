from __future__ import annotations

import argparse

from config import DOCS_DIR
from RAG_LOCAL.utils.embeddings import get_embeddings
from RAG_LOCAL.utils.loader import load_documents
from RAG_LOCAL.utils.splitter import split_documents
from RAG_LOCAL.utils.vectordb import create_vector_db


def ingest(docs_dir=DOCS_DIR, reset=True):
    documents = load_documents(docs_dir)
    chunks = split_documents(documents)

    if not chunks:
        raise RuntimeError("PDFs were loaded, but no chunks were created.")

    embedding = get_embeddings()
    create_vector_db(chunks, embedding, reset=reset)

    return {
        "documents": len(documents),
        "chunks": len(chunks),
        "docs_dir": str(docs_dir),
    }


def main():
    parser = argparse.ArgumentParser(description="Ingest PDF files into Chroma.")
    parser.add_argument(
        "--docs-dir",
        default=str(DOCS_DIR),
        help="Directory containing PDF files.",
    )
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append to the existing Chroma collection instead of rebuilding it.",
    )
    args = parser.parse_args()

    result = ingest(docs_dir=args.docs_dir, reset=not args.append)
    print(
        "Ingested {documents} PDF document pages into {chunks} chunks from {docs_dir}.".format(
            **result
        )
    )


if __name__ == "__main__":
    main()
