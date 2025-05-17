import json

def load_chunks():
    with open("chunks.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_available_sources():
    chunks = load_chunks()
    sources = sorted(set(chunk["source"] for chunk in chunks))
    return sources

def answer_question(question, source=None, secondary=None, detailed=False):
    chunks = load_chunks()
    results = []

    question = question.strip().lower()
    if source and source != "all":
        chunks = [c for c in chunks if c.get("source", "").lower() == source.lower()]
    if secondary:
        secondary = secondary.strip().lower()

    for chunk in chunks:
        text = chunk.get("content", "").lower()
        if question in text and (not secondary or secondary in text):
            results.append({
                "source": chunk.get("source", "Unknown"),
                "heading": chunk.get("heading", ""),  # fallback if missing
                "content": chunk.get("content", "")
            })

    return results
