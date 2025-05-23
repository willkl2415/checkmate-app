def answer_question(keyword, chunks, selected_document="", selected_section=""):
    keyword_lower = keyword.lower()
    keyword_tokens = set(keyword_lower.split())

    results = []

    for chunk in chunks:
        content = chunk.get("text", "").lower()
        document_match = selected_document == "" or chunk["document"] == selected_document
        section_match = selected_section == "" or chunk["section"] == selected_section

        if document_match and section_match:
            if keyword_lower in content or all(token in content for token in keyword_tokens):
                results.append({
                    "document": chunk["document"],
                    "section": chunk["section"],
                    "text": chunk["text"]
                })

    return results
