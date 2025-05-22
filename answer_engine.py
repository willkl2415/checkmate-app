import json

def load_chunks():
    with open("chunks.json", "r", encoding="utf-8") as f:
        return json.load(f)

def search_chunks(query, document_filter=None, section_filter=None):
    query = query.strip().lower()
    chunks = load_chunks()

    results = []
    for chunk in chunks:
        if query in chunk["text"].lower():
            if document_filter and chunk["document"] != document_filter:
                continue
            if section_filter and chunk["section"] != section_filter:
                continue
            results.append(chunk)

    return results
