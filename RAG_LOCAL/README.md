# PolicyLens RAG

PolicyLens RAG is a PDF question-answering project with two LLM paths:

- Local free mode using Ollama.
- Web API mode using an OpenAI-compatible chat completion endpoint.

Both modes share the same PDF ingestion pipeline: load PDFs, split them into chunks, embed them, store them in Chroma, retrieve the most relevant chunks, and answer only from that retrieved context.

## Project layout

- `app.py` - local Streamlit app with provider selector and PDF index rebuild button.
- `ingest.py` - CLI ingestion script for loading and chunking PDFs into Chroma.
- `query.py` - shared RAG retrieval and LLM answering logic.
- `utils/` - PDF loader, splitter, embeddings, prompt, and Chroma helpers.
- `HR_RAG_CLOUD/backend/` - FastAPI backend for cloud-style use.
- `HR_RAG_CLOUD/frontend/` - Streamlit frontend that calls the FastAPI backend.
- `HR_RAG_LOCAL/docs/` - place your PDF files here.

## Setup

Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create your local environment file:

```powershell
Copy-Item .env.example .env
```

Add PDFs to:

```text
HR_RAG_LOCAL/docs
```

## Build the PDF index

Run ingestion after adding or changing PDFs:

```powershell
python ingest.py
```

This loads PDFs, chunks them, embeds the chunks, and stores the vectors in `chroma_db`.

## Run with free local Ollama

Install Ollama, pull a model, and start Ollama:

```powershell
ollama pull llama3.2
```

Run the app:

```powershell
streamlit run app.py
```

Choose `Local Ollama` in the sidebar.

## Run with a web LLM

Set these values in `.env`:

```text
WEB_LLM_BASE_URL=https://api.openai.com/v1
WEB_LLM_API_KEY=your_api_key_here
WEB_LLM_MODEL=gpt-4o-mini
```

Then run:

```powershell
streamlit run app.py
```

Choose `Web API` in the sidebar.

Any OpenAI-compatible endpoint can be used by changing `WEB_LLM_BASE_URL` and `WEB_LLM_MODEL`.

## Cloud-style backend and frontend

Start the FastAPI backend:

```powershell
uvicorn HR_RAG_CLOUD.backend.api:app --reload
```

Start the cloud frontend in another terminal:

```powershell
streamlit run HR_RAG_CLOUD/frontend/app.py
```

The frontend calls `http://localhost:8000` by default. Change `POLICYLENS_API_URL` if your backend runs elsewhere.
