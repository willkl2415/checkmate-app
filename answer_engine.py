import json

def load_chunks():
    with open("chunks.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_available_sources(chunks):
    sources = sorted(set(chunk["source"] for chunk in chunks if "source" in chunk))
    return sources

def answer_question(chunks, query, source=None, secondary_keyword=None, detailed_only=False):
    results = []

    for chunk in chunks:
        if source and chunk.get("source") != source:
            continue
        if secondary_keyword and secondary_keyword.lower() not in chunk["content"].lower():
            continue
        if query.lower() in chunk["content"].lower():
            results.append({
                "chunk_id": chunk["chunk_id"],
                "filename": chunk["filename"],
                "source": chunk.get("source", "Unknown"),
                "heading": chunk.get("heading", ""),
                "content": chunk["content"]
            })

    if detailed_only:
        results = [r for r in results if len(r["content"].split()) > 40]

    return results
