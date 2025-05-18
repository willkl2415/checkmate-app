import re

def answer_question(query, chunks, keyword=None, secondary_keyword=None, detailed_only=False):
    results = []

    for chunk in chunks:
        text = chunk["text"]
        if detailed_only and len(text) < 100:
            continue

        match_found = False

        if keyword and secondary_keyword:
            if re.search(rf"\b{re.escape(keyword)}\b", text, re.IGNORECASE) and re.search(rf"\b{re.escape(secondary_keyword)}\b", text, re.IGNORECASE):
                match_found = True
        elif keyword:
            if re.search(rf"\b{re.escape(keyword)}\b", text, re.IGNORECASE):
                match_found = True
        elif secondary_keyword:
            if re.search(rf"\b{re.escape(secondary_keyword)}\b", text, re.IGNORECASE):
                match_found = True
        elif query:
            if re.search(rf"\b{re.escape(query)}\b", text, re.IGNORECASE):
                match_found = True

        if match_found:
            results.append({
                "source": chunk["source"],
                "content": text
            })

    return results


def get_available_sources(chunks):
    return sorted(list({chunk["source"] for chunk in chunks}))
