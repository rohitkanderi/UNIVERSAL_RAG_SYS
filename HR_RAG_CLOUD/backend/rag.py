from __future__ import annotations

from query import ask
from query import source_labels


def answer_question(question, provider="web", top_k=None):
    answer, docs = ask(question, provider=provider, top_k=top_k)

    return {
        "answer": answer,
        "sources": source_labels(docs),
    }
