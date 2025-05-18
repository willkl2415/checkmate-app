import json

def load_ingested_chunks():
    with open("chunks.json", "r", encoding="utf-8") as f:
        return json.load(f)

def answer_question(question, keyword="", section="All Sections", detailed=False, document="All"):
    with open("chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

    results = []
    question_lower = question.lower()
    keyword_lower = keyword.lower()

    for chunk in chunks:
        # Filter by section if selected
        if section != "All Sections" and chunk.get("section_title") != section:
            continue

        # Filter by document if selected
        if document != "All" and chunk.get("source") != document:
            continue

        # Apply query and keyword filters
        content_match = question_lower in chunk.get("content", "").lower()
        keyword_match = not keyword or keyword_lower in chunk.get("content", "").lower()

        if content_match and keyword_match:
            results.append(chunk)

    # Optionally reduce results
    if not detailed:
        for r in results:
            r["content"] = r["content"][:200] + "..." if len(r["content"]) > 200 else r["content"]

    return results
