import os
import json
import docx

SOURCE_DIR = "docs"
OUTPUT_FILE = "chunks.json"

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([para.text.strip() for para in doc.paragraphs if para.text.strip()])

def chunk_text(text, max_chunk_size=1000):
    sentences = text.split(". ")
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def extract_section(text):
    lines = text.splitlines()
    for line in lines:
        if line.strip() and any(char.isdigit() for char in line[:6]):
            return line.strip()
    return "Unknown"

def ingest_docs():
    all_chunks = []

    for filename in os.listdir(SOURCE_DIR):
        if filename.startswith("~$") or not filename.endswith(".docx"):
            continue

        filepath = os.path.join(SOURCE_DIR, filename)
        raw_text = extract_text_from_docx(filepath)
        chunks = chunk_text(raw_text)

        for chunk in chunks:
            section = extract_section(chunk)
            all_chunks.append({
                "document": filename,
                "section": section,
                "content": chunk
            })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"✅ Ingested {len(all_chunks)} chunks into {OUTPUT_FILE}")

if __name__ == "__main__":
    ingest_docs()
