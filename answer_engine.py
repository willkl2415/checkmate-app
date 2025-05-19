def answer_question(
    chunks,
    query="",
    keyword="",
    source_filter="All",
    section_filter="All",
    detailed=False
):
    results = []

    for chunk in chunks:
        # Apply filters
        if source_filter != "All" and chunk["document"] != source_filter:
            continue
        if section_filter != "All" and chunk["section"] != section_filter:
            continue

        match = False

        if query and query.lower() in chunk["content"].lower():
            match = True
        elif keyword and keyword.lower() in chunk["content"].lower():
            match = True

        if match:
            results.append({
                "document": chunk["document"],
                "section": chunk["section"],
                "content": chunk["content"] if detailed else chunk["content"].split(".")[0]
            })

    return results
