from __future__ import annotations

from RAG_LOCAL.query import normalize_provider


def supported_provider(provider):
    return normalize_provider(provider)
