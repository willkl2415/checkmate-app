import json

def load_chunks(path="chunks.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_available_sources():
    chunks = load_chunks()
    sources = sorted(set(chunk["source"] for chunk in chunks if "source" in chunk))
    return sources

def answer_question(question, source_filter=None, secondary_keyword=None, long_answers=True):
    chunks = load_chunks()
    matched_chunks = []

    for chunk in chunks:
        text = chunk["content"].lower()
        if question.lower() in text:
            if source_filter and chunk["source"] != source_filter:
                continue
            if secondary_keyword and secondary_keyword.lower() not in text:
                continue
            if long_answers and len(text) < 300:
                continue
            matched_chunks.append({
                "source": chunk["source"],
                "section": chunk.get("heading", ""),
                "text": chunk["content"]
            })

    return matched_chunks
