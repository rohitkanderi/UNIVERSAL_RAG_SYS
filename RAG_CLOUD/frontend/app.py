from __future__ import annotations

import os

import requests
import streamlit as st

from RAG_LOCAL.config import PROJECT_NAME
from RAG_LOCAL.config import RETRIEVAL_K

API_URL = os.getenv("POLICYLENS_API_URL", "http://localhost:8000")

st.set_page_config(page_title=f"{PROJECT_NAME} Cloud")

st.title(f"{PROJECT_NAME} Cloud")
st.caption("Frontend for the FastAPI RAG backend.")

with st.sidebar:
    st.header("Settings")
    api_url = st.text_input("API URL", value=API_URL)
    provider_label = st.radio("LLM provider", options=["Web API", "Local Ollama"])
    provider = "web" if provider_label == "Web API" else "ollama"
    top_k = st.slider("PDF chunks to retrieve", min_value=1, max_value=10, value=RETRIEVAL_K)

question = st.text_area("Ask a question about the PDFs", height=120)

if st.button("Ask"):
    try:
        response = requests.post(
            f"{api_url.rstrip('/')}/ask",
            json={
                "question": question,
                "provider": provider,
                "top_k": top_k,
            },
            timeout=90,
        )
        response.raise_for_status()
        payload = response.json()

        st.subheader("Answer")
        st.write(payload["answer"])

        st.subheader("Sources")
        for source in payload["sources"]:
            st.write(source)
    except Exception as exc:
        st.error(str(exc))
