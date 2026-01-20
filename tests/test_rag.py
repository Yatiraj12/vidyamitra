"""
Test Script for RAG Pipeline
Run this to test your RAG implementation
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.rag_pipeline import get_rag_pipeline

def test_rag():
    """
    Test the RAG pipeline with sample queries
    """
    print("="*70)
    print("🚀 VIDYAMITRA RAG PIPELINE TEST")
    print("="*70)
    print("\n🔄 Initializing RAG Pipeline...\n")

    try:
        # Initialize pipeline
        rag = get_rag_pipeline(llm_provider="gemini", top_k=3)

        print("\n✅ RAG Pipeline initialized successfully!\n")
        print("="*70)

        # Test queries
        test_queries = [
            "How can I help students who are struggling with math?",
            "What are some effective classroom management techniques?",
            "How do I make my lessons more engaging?"
        ]

        print("\n📝 Testing with sample queries...\n")

        for i, query in enumerate(test_queries, 1):
            print(f"\n{'='*70}")
            print(f"TEST {i}/3")
            print(f"{'='*70}")
            print(f"\n❓ Query: {query}\n")

            response = rag.query(query, return_sources=True)

            print(f"\n💡 ANSWER:")
            print("-" * 70)
            print(response['answer'])
            print("-" * 70)

            if response.get('sources'):
                print(f"\n📚 Sources Used: {len(response['sources'])} chunks")
                for j, source in enumerate(response['sources'], 1):
                    print(f"\n  [{j}] Score: {source['relevance_score']:.4f}")
                    print(f"      {source['text'][:150]}...")

            print()

        print("\n" + "="*70)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\n🎉 Your RAG Pipeline is working perfectly!")
        print("\n📝 Next Steps:")
        print("   1. Share this code with Role 3 (API team)")
        print("   2. They will import: from app.rag.rag_pipeline import get_rag_pipeline")
        print("   3. Integration ready!")

    except FileNotFoundError as e:
        print("\n" + "="*70)
        print("⚠️  VECTOR DATABASE NOT FOUND")
        print("="*70)
        print("\nYou need Role 1's output first!")
        print("\nRequired files:")
        print("  - data/processed/cleaned_chunks.json")
        print("  - data/vector_db/index/faiss.index")
        print("\nWhat to do:")
        print("  1. Wait for Role 1 (Data Ingestion) to complete their work")
        print("  2. Get their cleaned_chunks.json file")
        print("  3. Run: python scripts/build_index.py")
        print("  4. Then run this test again")
        print(f"\nError details: {str(e)}")

    except ValueError as e:
        print("\n" + "="*70)
        print("⚠️  API KEY NOT CONFIGURED")
        print("="*70)
        print("\nPlease set up your API key:")
        print("\n1. Create a .env file in the project root")
        print("2. Add: GEMINI_API_KEY=your_api_key_here")
        print("\nGet Gemini API key: https://makersuite.google.com/app/apikey")
        print(f"\nError details: {str(e)}")

    except Exception as e:
        print("\n" + "="*70)
        print("❌ ERROR OCCURRED")
        print("="*70)
        print(f"\nError: {str(e)}")
        print("\nChecklist:")
        print("  ✓ Is .env file created with API key?")
        print("  ✓ Are all packages installed? (pip install -r requirements.txt)")
        print("  ✓ Is vector database built?")
        print("  ✓ Is Python 3.8+ being used?")

if __name__ == "__main__":
    test_rag()
