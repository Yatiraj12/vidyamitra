"""
Vector Store Module for Vidyamitra
Handles embedding generation and vector database operations using FAISS
"""

import json
import os
import pickle
from typing import List, Dict

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


class VectorStore:
    def __init__(
        self,
        embedding_model_name: str =  "paraphrase-MiniLM-L3-v2",
        chunks_file: str = "data/processed/cleaned_chunks.json",
        index_dir: str = "data/vector_db/index",
    ):
        """
        Initialize vector store

        Args:
            embedding_model_name: SentenceTransformer model
            chunks_file: Path to cleaned chunks JSON
            index_dir: Directory to store FAISS index and metadata
        """
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.dimension = self.embedding_model.get_sentence_embedding_dimension()

        self.chunks_file = chunks_file
        self.index_dir = index_dir
        self.index_path = os.path.join(index_dir, "faiss.index")
        self.chunks_path = os.path.join(index_dir, "chunks.pkl")

        self.index = None
        self.chunks: List[Dict] = []

    # ---------------------------
    # Loading & Index Creation
    # ---------------------------
    def load_chunks(self):
        """Load text chunks from JSON file"""
        if not os.path.exists(self.chunks_file):
            raise FileNotFoundError(
                f"Chunks file not found: {self.chunks_file}"
            )

        with open(self.chunks_file, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        print(f"✅ Loaded {len(self.chunks)} chunks")

    def create_embeddings(self):
        """
        Generate embeddings and build FAISS cosine-similarity index
        """
        if not self.chunks:
            raise ValueError("No chunks loaded. Call load_chunks() first.")

        texts = [chunk.get("text", "") for chunk in self.chunks]

        print("🔄 Generating embeddings...")
        embeddings = self.embedding_model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True,
        ).astype("float32")

        # Normalize vectors for cosine similarity
        faiss.normalize_L2(embeddings)

        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(embeddings)

        print(f"✅ FAISS index created with {self.index.ntotal} vectors")

    def save_index(self):
        """Persist FAISS index and chunks"""
        if self.index is None:
            raise ValueError("Index not created yet")

        os.makedirs(self.index_dir, exist_ok=True)

        faiss.write_index(self.index, self.index_path)

        with open(self.chunks_path, "wb") as f:
            pickle.dump(self.chunks, f)

        print(f"✅ Vector store saved at {self.index_dir}")

    def load_index(self):
        """Load FAISS index and chunks from disk"""
        if not os.path.exists(self.index_path) or not os.path.exists(self.chunks_path):
            raise FileNotFoundError("Vector index or chunks not found")

        self.index = faiss.read_index(self.index_path)

        with open(self.chunks_path, "rb") as f:
            self.chunks = pickle.load(f)

        print(f"✅ Loaded vector store with {len(self.chunks)} chunks")

    # ---------------------------
    # Retrieval
    # ---------------------------
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieve top-k relevant chunks

        Args:
            query: Teacher query
            top_k: Number of chunks to return

        Returns:
            List of chunks with similarity scores
        """
        # ✅ FIX: DO NOT crash if index is missing (Render-safe)
        if self.index is None:
            print("⚠️ Vector index not loaded. Returning empty results.")
            return []

        query_embedding = self.embedding_model.encode(
            [query], convert_to_numpy=True
        ).astype("float32")

        faiss.normalize_L2(query_embedding)

        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.chunks):
                results.append(
                    {
                        "text": self.chunks[idx].get("text", ""),
                        "metadata": self.chunks[idx].get("metadata", {}),
                        "score": float(score),  # cosine similarity
                    }
                )

        return results


# ---------------------------
# Factory Function
# ---------------------------
def get_vector_store() -> VectorStore:
    """
    Factory method used by RAG pipeline
    """
    store = VectorStore()

    try:
        store.load_index()
    except FileNotFoundError:
        print("⚠️ Vector index not found. Run embedding creation first.")

    return store
