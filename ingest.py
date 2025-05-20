import os
import json
import docx

def extract_text_and_headings(doc_path):
    doc = docx.Document(doc_path)
    sections = []
    current_section = {"section": "Uncategorised", "text": ""}

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        if para.style.name.startswith("Heading"):
            if current_section["text"]:
                sections.append(current_section)
            current_section = {"section": text, "text": ""}
        else:
            current_section["text"] += " " + text

    if current_section["text"]:
        sections.append(current_section)

    return sections

def ingest_docs(folder_path="docs"):
    chunks = []
    for filename in os.listdir(folder_path):
        if filename.startswith("~$") or not filename.endswith(".docx"):
            continue
        full_path = os.path.join(folder_path, filename)
        sections = extract_text_and_headings(full_path)
        for sec in sections:
            chunks.append({
                "document": filename,
                "section": sec["section"],
                "content": sec["text"].strip()
            })
    return chunks

if __name__ == "__main__":
    all_chunks = ingest_docs()
    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)
