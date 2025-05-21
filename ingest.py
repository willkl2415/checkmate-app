import os
import docx
import json
import re

DOCS_FOLDER = "docs"
OUTPUT_FILE = "chunks.json"

def extract_paragraphs_by_heading(doc_path):
    doc = docx.Document(doc_path)
    chunks = []
    current_section = "Unknown Section"

    for para in doc.paragraphs:
        text = para.text.strip()
        style = para.style.name if para.style else ""

        if not text or text.startswith("Figure") or text.startswith("Table"):
            continue

        # Detect and update heading-style sections
        if "Heading" in style or re.match(r"^\d+(\.\d+)*\s+", text):
            current_section = text

        # Append the chunk with section and source
        chunks.append({
            "document": os.path.basename(doc_path),
            "section": current_section,
            "text": text
        })

    return chunks

def load_all_chunks_from_docs_folder():
    all_chunks = []
    for filename in os.listdir(DOCS_FOLDER):
        if filename.endswith(".docx") and not filename.startswith("~$"):
            file_path = os.path.join(DOCS_FOLDER, filename)
            all_chunks.extend(extract_paragraphs_by_heading(file_path))
    return all_chunks

if __name__ == "__main__":
    final_chunks = load_all_chunks_from_docs_folder()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_chunks, f, ensure_ascii=False, indent=2)
    print(f"{len(final_chunks)} chunks written to {OUTPUT_FILE}")
