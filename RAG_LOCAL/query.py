from __future__ import annotations

import gc

from config import DEFAULT_PROVIDER
from config import DB_DIR
from config import CHROMA_COLLECTION
from config import OLLAMA_BASE_URL
from config import OLLAMA_MODEL
from config import RETRIEVAL_K
from config import WEB_LLM_API_KEY
from config import WEB_LLM_BASE_URL
from config import WEB_LLM_MODEL
from config import WEB_LLM_TIMEOUT_SECONDS
from RAG_LOCAL.utils.embeddings import get_embeddings
from RAG_LOCAL.utils.prompting import build_rag_prompt


_embedding = None
_db = None


def get_vector_db():
    global _embedding
    global _db

    if _embedding is None:
        _embedding = get_embeddings()

    if _db is None:
        from langchain_chroma import Chroma

        _db = Chroma(
            persist_directory=str(DB_DIR),
            embedding_function=_embedding,
            collection_name=CHROMA_COLLECTION,
        )

    return _db


def reset_vector_db_cache():
    global _db

    _db = None
    gc.collect()


def normalize_provider(provider):
    requested = (provider or DEFAULT_PROVIDER).strip().lower()

    if requested in {"ollama", "local", "free"}:
        return "ollama"

    if requested in {"web", "cloud", "api", "openai"}:
        return "web"

    raise ValueError("Provider must be 'ollama' or 'web'.")


def ask(question, provider=None, top_k=None):
    clean_question = question.strip()
    if not clean_question:
        return "Please enter a question.", []

    selected_provider = normalize_provider(provider)
    docs = get_vector_db().similarity_search(clean_question, k=top_k or RETRIEVAL_K)
    if not docs:
        return (
            "I could not find matching PDF chunks. Run ingest.py after adding PDFs.",
            [],
        )

    prompt = build_rag_prompt(clean_question, docs)

    if selected_provider == "ollama":
        answer = _ask_ollama(prompt)
    else:
        answer = _ask_web_llm(prompt)

    return answer, docs


def _ask_ollama(prompt):
    import ollama

    client = ollama.Client(host=OLLAMA_BASE_URL)

    response = client.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]


def _ask_web_llm(prompt):
    import requests

    if not WEB_LLM_API_KEY:
        raise RuntimeError(
            "WEB_LLM_API_KEY is missing. Add it to .env to use the web LLM mode."
        )

    response = requests.post(
        f"{WEB_LLM_BASE_URL.rstrip('/')}/chat/completions",
        headers={
            "Authorization": f"Bearer {WEB_LLM_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": WEB_LLM_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "Answer only from the retrieved PDF context.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": 0.2,
        },
        timeout=WEB_LLM_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    payload = response.json()
    return payload["choices"][0]["message"]["content"]


def source_labels(docs):
    labels = []
    seen = set()

    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page")
        label = f"{source} page {page + 1}" if isinstance(page, int) else source

        if label not in seen:
            labels.append(label)
            seen.add(label)

    return labels
