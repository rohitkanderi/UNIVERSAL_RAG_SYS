from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent


def project_path(env_name, default):
    configured = Path(os.getenv(env_name, default))
    if configured.is_absolute():
        return configured
    return PROJECT_ROOT / configured


PROJECT_NAME = os.getenv("PROJECT_NAME", "PolicyLens RAG")
DOCS_DIR = project_path("DOCS_DIR", "HR_RAG_LOCAL/docs")
DB_DIR = project_path("DB_DIR", "chroma_db")
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "policylens_documents")

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))
RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "4"))

DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "ollama").lower()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

WEB_LLM_BASE_URL = os.getenv("WEB_LLM_BASE_URL", "https://api.openai.com/v1")
WEB_LLM_API_KEY = os.getenv("WEB_LLM_API_KEY", "")
WEB_LLM_MODEL = os.getenv("WEB_LLM_MODEL", "gpt-4o-mini")
WEB_LLM_TIMEOUT_SECONDS = int(os.getenv("WEB_LLM_TIMEOUT_SECONDS", "60"))
