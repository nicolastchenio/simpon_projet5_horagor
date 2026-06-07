# processing/matching/fuzzy_matcher.py

from typing import List
from difflib import SequenceMatcher
import re

from processing.matching.schema import MatchRecord
from processing.normalization.schema import FilmNormalized
from processing.matching.utils import normalize_title


class FuzzyMatcher:
    """
    Matching fuzzy (niveau 2/3) basé sur Titre + Année.
    Travaille EXCLUSIVEMENT sur FilmNormalized.
    """

    def __init__(self):
        self.counter = 0

    def _next_match_id(self) -> str:
        self.counter += 1
        return f"fuzzy_{self.counter:06d}"

    def is_match(self, a: FilmNormalized, b: FilmNormalized) -> bool:
        ta = normalize_title(a.title)
        tb = normalize_title(b.title)

        ya = a.release_year
        yb = b.release_year

        # Filtre année : si les deux ont une année, elles doivent être identiques
        if ya and yb and ya != yb:
            return False

        # Similarité textuelle sur le titre
        return SequenceMatcher(None, ta, tb).ratio() >= 0.92

    def match(
        self,
        tmdb_movies: List[FilmNormalized],
        external_movies: List[FilmNormalized],
        source_name: str = "kaggle",
    ) -> List[MatchRecord]:

        results = []

        for i, tmdb in enumerate(tmdb_movies):
            for j, ext in enumerate(external_movies):

                if not self.is_match(tmdb, ext):
                    continue

                results.append(
                    MatchRecord(
                        master_id=self._next_match_id(),
                        tmdb_index=i,
                        source_indices={source_name: j},
                        match_level=f"FUZZY_{source_name.upper()}",
                    )
                )

        return results