def answer_question(query, chunks, keyword=None, secondary_keyword=None, detailed_only=False):
    results = []

    for chunk in chunks:
        content_lower = chunk["content"].lower()
        query_lower = query.lower()
        keyword_lower = keyword.lower() if keyword else ""
        secondary_lower = secondary_keyword.lower() if secondary_keyword else ""

        matches_query = query_lower in content_lower if query_lower else True
        matches_keyword = keyword_lower in content_lower if keyword_lower else True
        matches_secondary = secondary_lower in content_lower if secondary_lower else True

        if matches_query and matches_keyword and matches_secondary:
            if detailed_only:
                if "1.1" in content_lower or "1.2" in content_lower or "analysis" in content_lower:
                    results.append(chunk)
            else:
                results.append(chunk)

    return results


def get_available_sources(chunks):
    return sorted(set(chunk["source"] for chunk in chunks))
