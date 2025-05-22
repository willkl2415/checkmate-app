def answer_question(keyword, chunks, selected_document="", selected_section=""):
    keyword_lower = keyword.lower()
    results = []

    for chunk in chunks:
        text = chunk.get("text", "").lower()
        doc = chunk.get("document", "")
        section = chunk.get("section", "")

        if keyword_lower in text:
            if (not selected_document or selected_document == doc) and \
               (not selected_section or selected_section == section):
                results.append({
                    "document": doc,
                    "section": section,
                    "text": chunk["text"]
                })

    return results
