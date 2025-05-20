import os
import docx
import json

def extract_text_with_headings(doc_path):
    doc = docx.Document(doc_path)
    content = []
    current_heading = "No Heading"

    for para in doc.paragraphs:
        if para.style.name.startswith("Heading"):
            current_heading = para.text.strip()
        elif para.text.strip():
            content.append({
                "document": os.path.basename(doc_path),
                "heading": current_heading,
                "text": para.text.strip()
            })

    return content

def ingest_documents(directory):
    all_chunks = []

    for filename in os.listdir(directory):
        if filename.endswith(".docx") and not filename.startswith("~$"):
            path = os.path.join(directory, filename)
            chunks = extract_text_with_headings(path)
            all_chunks.extend(chunks)

    return all_chunks

if __name__ == "__main__":
    docs_path = "docs"
    data = ingest_documents(docs_path)

    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Ingested {len(data)} content chunks.")
