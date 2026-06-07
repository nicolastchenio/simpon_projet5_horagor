# processing/matching/utils.py

import re
import unicodedata


def normalize_title(title: str) -> str:
    """
    Normalise un titre pour le matching.

    Exemple :
        "The Black Phone"
        -> "the black phone"

        "L'Étrange Noël"
        -> "l etrange noel"
    """

    if not title:
        return ""

    # minuscules
    title = title.lower()

    # suppression accents
    title = unicodedata.normalize("NFKD", title)
    title = "".join(
        c for c in title
        if not unicodedata.combining(c)
    )

    # suppression ponctuation
    title = re.sub(r"[^a-z0-9\s]", " ", title)

    # espaces multiples
    title = re.sub(r"\s+", " ", title)

    return title.strip()