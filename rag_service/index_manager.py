import faiss, os
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
DIM = 384

class DB:
    def __init__(self):
        self.index = faiss.IndexFlatL2(DIM)
        self.docs = []

    def add(self, text):
        emb = model.encode([text]).astype("float32")
        self.index.add(emb)
        self.docs.append(text)

    def search(self, q):
        emb = model.encode([q]).astype("float32")
        D,I = self.index.search(emb,5)
        return [self.docs[i] for i in I[0] if i < len(self.docs)]