from __future__ import annotations

from query import normalize_provider


def supported_provider(provider):
    return normalize_provider(provider)
