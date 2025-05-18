import os
import json
from docx import Document

SOURCE_DIR = "docs"
OUTPUT_FILE = "chunks.json"

def read_docx(file_path):
    try:
        doc = Document(file_path)
        text = []
        for para in doc.paragraphs:
            if para.text.strip():
                text.append(para.text.strip())
        return text
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def chunk_text(paragraphs, chunk_size=500):
    chunks = []
    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += para + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def ingest_docs():
    all_chunks = []
    for filename in os.listdir(SOURCE_DIR):
        if filename.startswith("~$") or not filename.endswith(".docx"):
            continue
        file_path = os.path.join(SOURCE_DIR, filename)
        paragraphs = read_docx(file_path)
        chunks = chunk_text(paragraphs)
        for chunk in chunks:
            all_chunks.append({
                "source": filename,
                "content": chunk
            })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    print(f"✅ Ingested {len(all_chunks)} chunks into {OUTPUT_FILE}")

if __name__ == "__main__":
    ingest_docs()
