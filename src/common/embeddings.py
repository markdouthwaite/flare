from typing import List, Any

import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel


def embed_document(doc: str, **kwargs: Any) -> np.ndarray:
    return embed_documents([doc], **kwargs)[0]


def embed_documents(
    docs: List[str], model_name: str = "BAAI/bge-small-en-v1.5"
) -> np.ndarray:
    """Embed the provided documents to create a document index"""
    # load the tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    # encode the docs with the tokenizer
    encoded_docs = tokenizer(docs, padding=True, truncation=True, return_tensors="pt")

    # generate your output embedding vectors
    with torch.no_grad():
        model_output = model(**encoded_docs)
        doc_embeddings = model_output[0][:, 0]

    # convert to numpy vectors for ease of use
    return doc_embeddings.numpy()
