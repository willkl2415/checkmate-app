def answer_question(question, chunks, source=None, secondary_keyword=None, detailed=False):
    question_lower = question.lower()
    results = []

    for chunk in chunks:
        content_lower = chunk["content"].lower()
        heading_lower = chunk.get("heading", "").lower()
        source_match = (source == "All" or chunk.get("source", "") == source)
        secondary_match = (not secondary_keyword or secondary_keyword.lower() in content_lower)

        if question_lower in content_lower and source_match and secondary_match:
            results.append({
                "source": chunk.get("source", "Unknown"),
                "heading": chunk.get("heading", "Untitled"),
                "content": chunk["content"] if detailed else None
            })

    return results  # If empty, app.py handles the fallback display
