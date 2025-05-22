def answer_question(keyword, chunks, selected_document="", selected_section=""):
    keyword = keyword.lower()
    words = keyword.split()
    results = []

    for chunk in chunks:
        content = chunk.get("text", "").lower()
        if (keyword in content or any(word in content for word in words)) and \
           (not selected_document or chunk["document"] == selected_document) and \
           (not selected_section or chunk["section"] == selected_section):

            results.append({
                "document": chunk["document"],
                "section": chunk["section"],
                "text": chunk["text"]
            })

    return results
