import math

def score_chunk(chunk: str, query: str) -> float:
    """Simple TF-IDF inspired scoring — no external ML dependencies."""
    query_words = set(query.lower().split())
    chunk_words = chunk.lower().split()
    chunk_word_count = len(chunk_words)

    if chunk_word_count == 0:
        return 0.0

    score = 0.0
    for word in query_words:
        term_freq = chunk_words.count(word) / chunk_word_count
        if term_freq > 0:
            score += term_freq * math.log(1 + 1 / term_freq)

    return score


def get_top_chunks(chunks: list[dict], query: str, top_k: int = 5) -> list[dict]:
    """Return the top_k most relevant chunks for the query."""
    scored = []

    for chunk in chunks:
        score = score_chunk(chunk["text"], query)
        scored.append({**chunk, "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]