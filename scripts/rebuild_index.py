"""
Build Vector Index Script
Run this after Role 1 completes data ingestion
"""

import sys
import os

# Ensure project root is on PYTHONPATH
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from app.retrieval.vector_store import VectorStore


def build_index():
    """
    Build vector index from cleaned chunks
    """
    print("=" * 70)
    print("🏗️  BUILDING VECTOR INDEX")
    print("=" * 70)

    chunks_path = "data/processed/cleaned_chunks.json"

    # Step 1: Check if cleaned chunks exist
    if not os.path.exists(chunks_path):
        print(f"\n❌ Error: {chunks_path} not found!")
        print("\nPlease ensure Role 1 (Data Ingestion) has completed their work.")
        print("Required file: data/processed/cleaned_chunks.json")
        return

    try:
        # Step 2: Initialize Vector Store
        print("\n🔄 Initializing Vector Store...")
        vector_store = VectorStore()

        # Step 3: Load chunks
        print("\n📂 Loading cleaned chunks...")
        vector_store.load_chunks()

        # Step 4: Create embeddings & FAISS index
        print("\n🧮 Creating embeddings...")
        print("(This may take a few minutes depending on data size)")
        vector_store.create_embeddings()

        # Step 5: Save index to disk
        print("\n💾 Saving vector index to disk...")
        vector_store.save_index()

        print("\n" + "=" * 70)
        print("✅ VECTOR INDEX BUILT SUCCESSFULLY!")
        print("=" * 70)
        print("\n📁 Index location: data/vector_db/index/")
        print("\nNext step:")
        print("👉 Start the API and test the RAG pipeline")

    except Exception as e:
        print(f"\n❌ Error while building index: {str(e)}")
        print("\nPlease check:")
        print("  - cleaned_chunks.json is valid JSON")
        print("  - 'text' field exists in each chunk")
        print("  - sentence-transformers & faiss are installed")
        print("  - You have write permissions")


if __name__ == "__main__":
    build_index()
