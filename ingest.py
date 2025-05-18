import os
import json
import docx

CHUNK_SIZE = 800
SOURCE_DIR = "docs"

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return [para.text.strip() for para in doc.paragraphs if para.text.strip()]

def split_into_chunks(paragraphs, size):
    chunks = []
    current_chunk = ""
    current_heading = "No heading found"
    
    for para in paragraphs:
        if para[:3].strip().isdigit() or para[:2].strip().isdigit():
            current_heading = para
        
        if len(current_chunk) + len(para) <= size:
            current_chunk += para + " "
        else:
            chunks.append((current_heading, current_chunk.strip()))
            current_chunk = para + " "

    if current_chunk:
        chunks.append((current_heading, current_chunk.strip()))
        
    return chunks

def ingest_docs():
    all_chunks = []
    
    for filename in os.listdir(SOURCE_DIR):
        if filename.endswith(".docx") and not filename.startswith("~$"):
            file_path = os.path.join(SOURCE_DIR, filename)
            paragraphs = extract_text_from_docx(file_path)
            chunk_tuples = split_into_chunks(paragraphs, CHUNK_SIZE)
            
            for i, (heading, content) in enumerate(chunk_tuples):
                all_chunks.append({
                    "source": filename,
                    "heading": heading,
                    "content": content,
                    "chunk_id": f"{filename}_chunk_{i+1}"
                })

    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"✅ Ingested {len(all_chunks)} chunks into chunks.json")

if __name__ == "__main__":
    ingest_docs()
