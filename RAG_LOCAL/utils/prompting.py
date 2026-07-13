from __future__ import annotations


def build_rag_prompt(question, documents):
    context = "\n\n".join(
        f"Source: {doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
        for doc in documents
    )

    return f"""You are PolicyLens RAG, a careful document-grounded assistant.

Answer the user's question using only the context below.
If the answer is not present in the context, say you do not know from the provided PDFs.
Keep the answer concise and cite the source filenames when useful.

Context:
{context}

Question:
{question}

Answer:"""
