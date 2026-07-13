from RAG_LOCAL.config import CHUNK_OVERLAP
from RAG_LOCAL.config import CHUNK_SIZE


def split_documents(documents):
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    return splitter.split_documents(documents)
