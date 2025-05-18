import json

def load_ingested_chunks():
    try:
        with open("chunks.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Failed to load chunks.json:", e)
        return []

def answer_question(question, keyword=None, section=None, detailed=False):
    question = question.lower()
    chunks = load_ingested_chunks()
    results = []

    for chunk in chunks:
        content = chunk.get("content", "").lower()
        match_score = 0

        if question in content:
            match_score += 2
        elif any(q_word in content for q_word in question.split()):
            match_score += 1

        if keyword:
            keyword = keyword.lower()
            if keyword in content:
                match_score += 1

        if section and section != "All Sections":
            section_title = chunk.get("section_title", "").lower()
            if section.lower() not in section_title:
                continue  # skip this chunk if section doesn't match

        if match_score > 0:
            result = {
                "source": chunk.get("source", "Unknown"),
                "section": chunk.get("section_title", "Unknown"),
                "content": chunk.get("content", "No content found"),
            }
            results.append(result)

    # Sort results by match_score descending
    return sorted(results, key=lambda x: x["content"].count(question), reverse=True)
