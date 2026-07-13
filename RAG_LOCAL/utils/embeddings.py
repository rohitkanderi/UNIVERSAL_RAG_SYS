from RAG_LOCAL.config import EMBEDDING_MODEL


def get_embeddings():
    from langchain_huggingface import HuggingFaceEmbeddings

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )
