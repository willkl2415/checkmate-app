from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def answer_question(chunks, query="", keyword="", document_filter="All", section_filter="All", detailed=False):
    results = []
    seen = set()

    for chunk in chunks:
        if document_filter != "All" and chunk["document"] != document_filter:
            continue
        if section_filter != "All" and chunk["section"] != section_filter:
            continue

        if query and (query.lower() in chunk["content"].lower() or similar(query.lower(), chunk["content"].lower()) > 0.6):
            match_key = (chunk["document"], chunk["section"], chunk["content"][:60])
            if match_key not in seen:
                results.append(chunk)
                seen.add(match_key)
        elif keyword and keyword.lower() in chunk["content"].lower():
            match_key = (chunk["document"], chunk["section"], chunk["content"][:60])
            if match_key not in seen:
                results.append(chunk)
                seen.add(match_key)

    return results
