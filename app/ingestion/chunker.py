def chunk_text(text, chunk_size=400):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk_words = words[i:i + chunk_size]
        chunk_text = " ".join(chunk_words)

        chunks.append({
            "content": chunk_text,
            "metadata": {
                "source": "NCERT",
                "category": "pedagogy",
                "language": "English"
            }
        })

    return chunks
