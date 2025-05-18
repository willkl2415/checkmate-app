import os
import json
import docx

CHUNK_SIZE = 800  # characters

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text.strip() for para in doc.paragraphs if para.text.strip()])

def split_into_chunks(text, size):
    return [text[i:i+size] for i in range(0, len(text), size)]

def load_documents(folder="."):
    docs = []
    for filename in os.listdir(folder):
        if filename.endswith(".docx") and not filename.startswith("~$"):
            full_path = os.path.join(folder, filename)
            text = extract_text_from_docx(full_path)
            chunks = split_into_chunks(text, CHUNK_SIZE)
            for i, chunk in enumerate(chunks):
                docs.append({
                    "source": filename,
                    "heading": f"Section {i+1}",
                    "content": chunk,
                    "chunk_id": f"{filename}_chunk_{i+1}"
                })
    return docs

if __name__ == "__main__":
    all_chunks = load_documents()
    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)
    print(f"✅ Ingested {len(all_chunks)} chunks into chunks.json")
