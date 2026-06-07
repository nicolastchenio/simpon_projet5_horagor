# processing/matching/schema.py

from dataclasses import dataclass, field
from typing import Optional, Dict


@dataclass
class MatchRecord:
    """
    Représente un film reconnu comme étant la même entité
    entre plusieurs sources.
    """

    master_id: str
    tmdb_index: int

    # Dictionnaire des index par source : {"kaggle": 12, "imdb": 5, ...}
    source_indices: Dict[str, int] = field(default_factory=dict)

    match_level: str = ""