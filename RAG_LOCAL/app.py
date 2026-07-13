import streamlit as st

from config import DB_DIR
from config import DOCS_DIR
from config import OLLAMA_MODEL
from config import PROJECT_NAME
from config import RETRIEVAL_K
from config import WEB_LLM_API_KEY
from config import WEB_LLM_MODEL
from ingest import ingest
from query import ask
from query import reset_vector_db_cache
from query import source_labels

st.set_page_config(page_title=PROJECT_NAME)

st.title(PROJECT_NAME)
st.caption("Ask questions over your PDF documents using either local Ollama or a web LLM.")

with st.sidebar:
    st.header("Settings")
    provider_label = st.radio(
        "LLM provider",
        options=["Local Ollama", "Web API"],
        help="Local Ollama is free and runs on your machine. Web API uses your configured API key.",
    )
    provider = "ollama" if provider_label == "Local Ollama" else "web"
    top_k = st.slider("PDF chunks to retrieve", min_value=1, max_value=10, value=RETRIEVAL_K)

    st.markdown("---")
    st.write(f"PDF folder: `{DOCS_DIR}`")
    st.write(f"Vector DB: `{DB_DIR}`")

    if provider == "ollama":
        st.write(f"Ollama model: `{OLLAMA_MODEL}`")
    else:
        st.write(f"Web model: `{WEB_LLM_MODEL}`")
        if not WEB_LLM_API_KEY:
            st.warning("Set WEB_LLM_API_KEY in .env before using Web API mode.")

    if st.button("Rebuild PDF index"):
        reset_vector_db_cache()
        with st.spinner("Loading, chunking, embedding, and storing PDFs..."):
            result = ingest()
        reset_vector_db_cache()
        st.success(
            "Indexed {documents} loaded PDF pages into {chunks} chunks.".format(**result)
        )

question = st.text_area("Ask a question about the PDFs", height=120)

if st.button("Ask"):
    try:
        with st.spinner("Retrieving PDF chunks and asking the selected LLM..."):
            answer, docs = ask(question, provider=provider, top_k=top_k)

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Sources")
        if docs:
            for source in source_labels(docs):
                st.write(source)
        else:
            st.write("No sources returned.")
    except Exception as exc:
        st.error(str(exc))
