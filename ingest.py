import os
import json
import re
from docx import Document

def extract_text_with_sections(doc_path):
    document = Document(doc_path)
    chunks = []

    current_heading = "No Heading"
    filename = os.path.basename(doc_path)

    # Process all paragraphs and heading patterns
    for para in document.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # Detect and assign heading
        if re.match(r"^\d+(\.\d+)*\s", text):
            current_heading = text

        chunks.append({
            "document": filename,
            "heading": current_heading,
            "content": text
        })

    # Process all tables
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    text = para.text.strip()
                    if text:
                        chunks.append({
                            "document": filename,
                            "heading": current_heading,
                            "content": text
                        })

    return chunks

def main():
    docs_dir = "docs"
    output_file = "chunks.json"
    all_chunks = []

    for file in os.listdir(docs_dir):
        if file.endswith(".docx") and not file.startswith("~$"):
            full_path = os.path.join(docs_dir, file)
            all_chunks.extend(extract_text_with_sections(full_path))

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"✅ chunks.json created with {len(all_chunks)} total entries")

if __name__ == "__main__":
    main()
