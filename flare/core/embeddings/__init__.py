from numpy import ndarray
from sentence_transformers import SentenceTransformer


def embed_text(text: str, path: str) -> ndarray:
    model = SentenceTransformer(path)
    embeddings = model.encode([text])
    return embeddings[0]
