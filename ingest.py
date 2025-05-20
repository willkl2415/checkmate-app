import os
import json
import docx

SOURCE_DIR = "docs"
OUTPUT_FILE = "chunks.json"
MAX_CHUNK_SIZE = 1000

def extract_text_from_docx(path):
    doc = docx.Document(path)
    full_text = []
    for para in doc.paragraphs:
        if para.text.strip():
            full_text.append(para.text.strip())
    return full_text

def chunk_text_by_paragraph(text_blocks, max_chunk_size=MAX_CHUNK_SIZE):
    chunks = []
    current_chunk = []
    current_length = 0
    for paragraph in text_blocks:
        if current_length + len(paragraph) > max_chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(paragraph)
        current_length += len(paragraph)
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def get_section_from_text(text):
    import re
    match = re.search(r'\b\d+(\.\d+)*\b', text)
    return match.group(0) if match else "Uncategorised"

def ingest_docs():
    all_chunks = []
    for filename in os.listdir(SOURCE_DIR):
        if not filename.endswith(".docx") or filename.startswith("~$"):
            continue
        filepath = os.path.join(SOURCE_DIR, filename)
        try:
            text_blocks = extract_text_from_docx(filepath)
            paragraph_chunks = chunk_text_by_paragraph(text_blocks)
            for chunk in paragraph_chunks:
                section = get_section_from_text(chunk)
                all_chunks.append({
                    "document": filename,
                    "section": section,
                    "content": chunk
                })
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)
    print(f"✅ Ingested {len(all_chunks)} chunks into {OUTPUT_FILE}")

if __name__ == "__main__":
    ingest_docs()
