import re

import numpy as np
from langchain_core.tools import tool
import requests

import ollama

from crm_chatbot.resource_loader import ResourceLoader

faq_text = ResourceLoader.read_text_resource("swiss_faq.md")
docs = [{"page_content": txt} for txt in re.split(r"(?=\n##)", faq_text)]

embedding_mode = "snowflake-arctic-embed"

class VectorStoreRetriever:
    def __init__(self, docs: list, vectors: list):
        self._arr = np.array(vectors)
        self._docs = docs

    @classmethod
    def from_docs(cls, docs: list[dict]) -> "VectorStoreRetriever":
        embeddings = [ollama.embeddings(model=embedding_mode, prompt=doc["page_content"]) for doc in docs]
        vectors = [emb["embedding"] for emb in embeddings]
        return cls(docs, vectors)

    def query(self, query: str, k: int = 5) -> list[dict]:
        embed = ollama.embeddings(
            model=embedding_mode, prompt=query
        )
        # "@" is just a matrix multiplication in python
        scores = np.array(embed['embedding']) @ self._arr.T
        top_k_idx = np.argpartition(scores, -k)[-k:]
        top_k_idx_sorted = top_k_idx[np.argsort(-scores[top_k_idx])]
        return [
            {**self._docs[idx], "similarity": scores[idx]} for idx in top_k_idx_sorted
        ]

retriever = VectorStoreRetriever.from_docs(docs)

@tool
def lookup_policy(query: str) -> str:
    """Consult the company policies to check whether certain options are permitted.
    Use this before making any flight changes performing other 'write' events."""
    docs = retriever.query(query, k=2)
    return "\n\n".join([doc["page_content"] for doc in docs])

if __name__ == "__main__":
    print(lookup_policy("tchanging flight dates to next week"))