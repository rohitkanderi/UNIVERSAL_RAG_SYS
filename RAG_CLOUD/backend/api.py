from __future__ import annotations

from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import Field

from RAG_LOCAL.config import PROJECT_NAME
from RAG_LOCAL.config import RETRIEVAL_K
from RAG_CLOUD.backend.rag import answer_question

app = FastAPI(title=f"{PROJECT_NAME} API")


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)
    provider: str = Field(default="web")
    top_k: int = Field(default=RETRIEVAL_K, ge=1, le=10)


class AskResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/health")
def health():
    return {"status": "ok", "service": PROJECT_NAME}


@app.post("/ask", response_model=AskResponse)
def ask_endpoint(request: AskRequest):
    try:
        return answer_question(
            question=request.question,
            provider=request.provider,
            top_k=request.top_k,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
