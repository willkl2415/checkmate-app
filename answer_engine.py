
def answer_question(keyword, selected_source, secondary_keyword, chunks, detailed_only):
    keyword = keyword.lower()
    secondary_keyword = secondary_keyword.lower()
    results = []

    for chunk in chunks:
        text = chunk["text"].lower()
        if keyword in text and (selected_source == "All" or chunk["source"] == selected_source):
            if secondary_keyword:
                if secondary_keyword in text:
                    results.append(chunk)
            else:
                results.append(chunk)

    if detailed_only:
        results = [r for r in results if len(r["text"].split()) > 40]

    return results

def get_available_sources(chunks):
    sources = set()
    for chunk in chunks:
        sources.add(chunk["source"])
    return sorted(sources)
