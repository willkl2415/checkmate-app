import os
import json
import re
from docx import Document

def extract_chunks_with_sections(doc_path):
    document = Document(doc_path)
    chunks = []

    current_section = "No Heading"
    for para in document.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # Detect section heading using numbered pattern (e.g. 1.1, 2.3.4, etc.)
        if re.match(r"^\d+(\.\d+)*\s", text):
            current_section = text

        chunks.append({
            "document": os.path.basename(doc_path),
            "section": current_section,
            "text": text
        })

    return chunks

def main():
    docs_folder = "docs"
    output_file = "chunks.json"
    all_chunks = []

    for filename in os.listdir(docs_folder):
        if filename.endswith(".docx") and not filename.startswith("~$"):
            doc_path = os.path.join(docs_folder, filename)
            chunks = extract_chunks_with_sections(doc_path)
            all_chunks.extend(chunks)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"✅ chunks.json generated with {len(all_chunks)} entries.")

if __name__ == "__main__":
    main()
