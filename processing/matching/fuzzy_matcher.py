# processing/matching/fuzzy_matcher.py

from typing import List, Any
from difflib import SequenceMatcher
import re

from processing.matching.schema import MatchRecord


class FuzzyMatcher:
    """
    Matching fuzzy compatible :
    - FilmNormalized (Pydantic)
    - dict (tests legacy)
    """

    def __init__(self):
        self.counter = 0

    # --------------------------------------------------
    # ID generator
    # --------------------------------------------------
    def _next_match_id(self) -> str:
        self.counter += 1
        return f"fuzzy_{self.counter:06d}"

    # --------------------------------------------------
    # SAFE ACCESSORS (clé correction)
    # --------------------------------------------------
    def _get_title(self, movie: Any) -> str:
        if isinstance(movie, dict):
            return movie.get("title", "")
        return getattr(movie, "title", "")

    def _get_year(self, movie: Any):
        if isinstance(movie, dict):
            return movie.get("release_year")
        return getattr(movie, "release_year", None)

    def _get_date(self, movie: Any):
        if isinstance(movie, dict):
            return movie.get("release_date")
        return getattr(movie, "release_date", None)

    # --------------------------------------------------
    # normalize
    # --------------------------------------------------
    def normalize_title(self, title: str) -> str:
        if not title:
            return ""

        title = title.lower()
        title = re.sub(r"[^a-z0-9\s]", "", title)
        title = re.sub(r"\s+", " ", title).strip()

        return title

    # --------------------------------------------------
    # year extraction SAFE
    # --------------------------------------------------
    def extract_year(self, movie: Any):
        if not movie:
            return None

        year = self._get_year(movie)
        if year:
            return year

        date = self._get_date(movie)
        if isinstance(date, str):
            m = re.search(r"\d{4}", date)
            return int(m.group()) if m else None

        return None

    # --------------------------------------------------
    # similarity
    # --------------------------------------------------
    def similarity(self, a: str, b: str) -> float:
        return SequenceMatcher(None, a, b).ratio()

    # --------------------------------------------------
    # MAIN MATCH LOGIC
    # --------------------------------------------------
    def is_match(self, a: Any, b: Any) -> bool:

        ta = self.normalize_title(self._get_title(a))
        tb = self.normalize_title(self._get_title(b))

        ya = self.extract_year(a)
        yb = self.extract_year(b)

        if ya and yb and ya != yb:
            return False

        return self.similarity(ta, tb) >= 0.92

    # --------------------------------------------------
    # PIPELINE MODE (Pydantic)
    # --------------------------------------------------
    def match(
        self,
        tmdb_movies: List[Any],
        external_movies: List[Any],
        source_name: str = "kaggle",
    ) -> List[MatchRecord]:

        results = []

        for i, tmdb in enumerate(tmdb_movies):
            for j, ext in enumerate(external_movies):

                if not self.is_match(tmdb, ext):
                    continue

                record = MatchRecord(
                    master_id=self._next_match_id(),
                    tmdb_index=i,
                    match_level=f"FUZZY_{source_name.upper()}",
                )

                if source_name == "kaggle":
                    record.kaggle_index = j
                elif source_name == "imdb":
                    record.imdb_index = j
                elif source_name == "rotten":
                    record.rotten_index = j

                results.append(record)

        return results

    # --------------------------------------------------
    # LEGACY TEST MODE (dict output)
    # --------------------------------------------------
    def match_all(self, source_a, source_b):
        """
        Retour simple pour test :
        [(i, j)]
        """

        matches = []

        for i, a in enumerate(source_a):
            for j, b in enumerate(source_b):

                if self.is_match(a, b):
                    matches.append((i, j))

        return matches