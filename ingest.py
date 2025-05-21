import re
import os
import json
import docx

def extract_paragraphs_by_heading(doc_path):
    doc = docx.Document(doc_path)
    chunks = []
    current_heading = "No Heading"
    heading_pattern = r"^\d+(\.\d+)*"

    for para in doc.paragraphs:
        text = para.text.strip()

        if not text:
            continue

        if para.style.name.startswith("Heading") or re.match(heading_pattern, text):
            current_heading = text

        chunks.append({
            "document": os.path.basename(doc_path),
            "heading": current_heading,
            "content": text
        })

    return chunks

def load_all_chunks_from_docs_folder():
    all_chunks = []
    docs_folder = "docs"

    for filename in os.listdir(docs_folder):
        if filename.endswith(".docx") and not filename.startswith("~$"):
            file_path = os.path.join(docs_folder, filename)
            all_chunks.extend(extract_paragraphs_by_heading(file_path))

    return all_chunks

if __name__ == "__main__":
    final_chunks = load_all_chunks_from_docs_folder()
    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(final_chunks, f, indent=2, ensure_ascii=False)
    print(f"Ingested {len(final_chunks)} chunks.")
