import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from app.ingestion.pdf_loader import load_pdf_text
from app.ingestion.text_cleaner import clean_text
from app.ingestion.chunker import chunk_text

PDF_PATH = "data/raw/ncert_training_resource.txt"

# PDF_PATH = "data/raw/ncert_training_resource.pdf"
OUTPUT_PATH = "data/processed/cleaned_chunks.json"

def run():
    raw_text = load_pdf_text(PDF_PATH)
    cleaned_text = clean_text(raw_text)
    chunks = chunk_text(cleaned_text)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print("✅ Ingestion complete")
    print(f"Total chunks: {len(chunks)}")

if __name__ == "__main__":
    run()

