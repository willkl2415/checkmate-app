def answer_question(chunks, query="", keyword="", source_filter="All", section_filter="All", detailed=True):
    results = []
    query = query.lower()
    keyword = keyword.lower()

    for chunk in chunks:
        if source_filter != "All" and chunk["document"] != source_filter:
            continue
        if section_filter != "All" and chunk["section"] != section_filter:
            continue

        match = False
        if query and query in chunk["content"].lower():
            match = True
        elif keyword and keyword in chunk["content"].lower():
            match = True

        if match:
            results.append({
                "document": chunk["document"],
                "section": chunk["section"],
                "content": chunk["content"]
            })

    return results
