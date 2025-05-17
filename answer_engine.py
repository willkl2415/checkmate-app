import re
from ingest import load_documents

def search_documents(primary_query, secondary_keyword=None, min_length=None, selected_source=None):
    """
    Searches loaded documents for matches based on primary and secondary keywords, length filter, and source filter.
    Returns a list of relevant result dictionaries.
    """
    results = []
    query = primary_query.strip().lower()
    secondary = secondary_keyword.strip().lower() if secondary_keyword else None

    all_docs = load_documents()

    for doc in all_docs:
        source = doc['source']
        section = doc['section']
        text = doc['text']
        text_lower = text.lower()

        if query in text_lower:
            if secondary and secondary not in text_lower:
                continue
            if min_length and len(text.strip()) < min_length:
                continue
            if selected_source and selected_source.lower() != source.lower():
                continue

            results.append({
                "source": source,
                "section": section,
                "text": text
            })

    return results

def get_available_sources():
    """
    Returns a sorted list of all .txt filenames inside the 'chunks' folder.
    """
    import os
    return sorted([f for f in os.listdir("chunks") if f.endswith(".txt")])
