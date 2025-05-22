import os
import json
import docx
import re

known_headings_file = "known_headings.json"

def load_known_headings():
    if os.path.exists(known_headings_file):
        with open(known_headings_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def extract_chunks(doc_path):
    doc = docx.Document(doc_path)
    chunks = []
    current_section = None
    buffer = []

    filename = os.path.basename(doc_path)
    known_headings = load_known_headings()

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        match = next((h for h in known_headings if text.startswith(h)), None)
        if match:
            if buffer:
                chunks.append({
                    "document": filename,
                    "section": current_section if current_section else "Unknown Section",
                    "text": " ".join(buffer)
                })
                buffer = []
            current_section = match
        buffer.append(text)

    if buffer:
        chunks.append({
            "document": filename,
            "section": current_section if current_section else "Unknown Section",
            "text": " ".join(buffer)
        })

    return chunks

def load_all_chunks_from_docs_folder():
    docs_folder = "docs"
    all_chunks = []
    for filename in os.listdir(docs_folder):
        if filename.endswith(".docx") and not filename.startswith("~$"):
            path = os.path.join(docs_folder, filename)
            all_chunks.extend(extract_chunks(path))
    return all_chunks

def main():
    all_chunks = load_all_chunks_from_docs_folder()
    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
