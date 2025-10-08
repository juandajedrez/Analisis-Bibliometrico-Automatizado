from typing import Set


def generate_ngrams(text: str, n: int) -> Set[str]:
    """
    Generate the set of n‑grams from the given text.

    Args:
        text: The input string.
        n: The length of each n‑gram (must be > 0).

    Returns:
        A set of substrings, each of length n. If n is greater than
        the length of text, returns an empty set.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    lowered = text.lower()
    length = len(lowered)
    if length < n:
        return set()
    return {lowered[i : i + n] for i in range(length - n + 1)}


def jaccard_distance(s1: str, s2: str, n: int = 2) -> float:
    """
    Compute the Jaccard distance between two strings, by interpreting
    each string as the set of its n‑grams.

    Args:
        s1: First input string.
        s2: Second input string.
        n: The size of n‑grams (default: 2, i.e. bigrams).

    Returns:
        A float in [0, 1]. 0 means identical (in terms of n‑grams),
        1 means completely disjoint in terms of n‑grams.
    """
    grams1 = generate_ngrams(s1, n)
    grams2 = generate_ngrams(s2, n)

    intersection = grams1.intersection(grams2)
    union = grams1.union(grams2)

    if not union:
        # Edge case: no n‑grams at all (e.g. both strings shorter than n)
        return 0.0

    similarity = len(intersection) / len(union)
    return 1.0 - similarity
