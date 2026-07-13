from __future__ import annotations

import contextlib
from pathlib import Path

from RAG_LOCAL.config import CHROMA_COLLECTION
from RAG_LOCAL.config import DB_DIR


def create_vector_db(chunks, embedding, reset=False):
    from langchain_chroma import Chroma

    db_path = Path(DB_DIR)

    db_path.mkdir(parents=True, exist_ok=True)

    if reset:
        with contextlib.suppress(Exception):
            existing_db = Chroma(
                persist_directory=str(db_path),
                embedding_function=embedding,
                collection_name=CHROMA_COLLECTION,
            )
            existing_db.delete_collection()

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=str(db_path),
        collection_name=CHROMA_COLLECTION,
    )

    return db


def load_vector_db(embedding):
    from langchain_chroma import Chroma

    db_path = Path(DB_DIR)

    return Chroma(
        persist_directory=str(db_path),
        embedding_function=embedding,
        collection_name=CHROMA_COLLECTION,
    )
