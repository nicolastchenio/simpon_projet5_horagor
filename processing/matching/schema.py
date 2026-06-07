# processing/matching/schema.py

from dataclasses import dataclass
from typing import Optional


@dataclass
class MatchRecord:
    """
    Représente un film reconnu comme étant la même entité
    entre plusieurs sources.

    Cette structure sera utilisée par la phase de matching.

    La fusion viendra plus tard.
    """

    master_id: str

    tmdb_index: Optional[int] = None
    kaggle_index: Optional[int] = None
    imdb_index: Optional[int] = None
    rotten_index: Optional[int] = None

    match_level: str = ""