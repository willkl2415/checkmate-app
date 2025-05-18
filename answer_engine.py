import json

def load_chunks(filepath="chunks.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def get_available_sources(chunks):
    return sorted(set(chunk.get("source", "Unknown") for chunk in chunks))

def answer_question(chunks, question, document_filter=None, secondary_keyword=None, show_detailed=False):
    results = []

    # Sanitize input
    question_keywords = [kw.strip().lower() for kw in question.split() if kw.strip()]
    secondary_keywords = [kw.strip().lower() for kw in secondary_keyword.split()] if secondary_keyword else []

    for chunk in chunks:
        content = chunk.get("content", "").lower()
        source = chunk.get("source", "Unknown")
        heading = chunk.get("heading", "No heading")

        if document_filter and source != document_filter:
            continue

        match_score = 0
        match_score += sum(content.count(kw) for kw in question_keywords)
        match_score += sum(content.count(kw) for kw in secondary_keywords)

        if match_score > 0:
            results.append({
                "source": source,
                "heading": heading,
                "content": chunk.get("content", ""),
                "score": match_score
            })

    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)

    return results if show_detailed else results[:3]
