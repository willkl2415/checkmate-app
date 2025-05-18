import json
import re

def load_chunks(filepath="chunks.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def get_available_sources(chunks):
    sources = sorted(set(chunk["source"] for chunk in chunks if "source" in chunk))
    return sources

def answer_question(chunks, question, document_filter=None, secondary_keyword=None, show_detailed=False):
    results = []

    # Prepare case-insensitive keyword matching
    question_keywords = [kw.strip().lower() for kw in question.split()]
    secondary_keywords = [kw.strip().lower() for kw in secondary_keyword.split()] if secondary_keyword else []

    for chunk in chunks:
        if document_filter and chunk.get("source") != document_filter:
            continue

        content = chunk.get("content", "").lower()
        heading = chunk.get("heading", "")
        match_score = 0

        # Count matches for primary and secondary keywords
        match_score += sum(content.count(kw) for kw in question_keywords)
        match_score += sum(content.count(kw) for kw in secondary_keywords)

        if match_score > 0:
            results.append({
                "source": chunk.get("source", "Unknown"),
                "heading": heading,
                "content": chunk.get("content", ""),
                "score": match_score
            })

    # Sort by best match
    results.sort(key=lambda x: x["score"], reverse=True)

    if show_detailed:
        return results
    else:
        return results[:3]
