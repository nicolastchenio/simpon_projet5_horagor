# processing/matching/id_matcher.py

from typing import List
from processing.matching.schema import MatchRecord
from processing.matching.utils import normalize_title


class IDMatcher:
    """
    Matching basé sur identifiants :
    - tmdb_id
    - imdb_id
    """

    def __init__(self):
        self.counter = 0

    def _next_match_id(self) -> str:
        self.counter += 1
        return f"id_{self.counter:06d}"

    # --------------------------------------------------
    # TMDB ID
    # --------------------------------------------------
    def match_by_tmdb_id(self, tmdb_movies, kaggle_movies):

        matches = []

        # index kaggle
        kaggle_index = {}

        for i, m in enumerate(kaggle_movies):

            tmdb_id = m.ids.tmdb_id   # ✔ Pydantic access

            if tmdb_id is not None:
                kaggle_index[tmdb_id] = (i, m)

        # match tmdb
        for tmdb_idx, tmdb in enumerate(tmdb_movies):

            tmdb_id = tmdb.ids.tmdb_id

            if tmdb_id is None:
                continue

            if tmdb_id not in kaggle_index:
                continue

            kaggle_idx, kaggle = kaggle_index[tmdb_id]

            if normalize_title(tmdb.title) != normalize_title(kaggle.title):
                continue

            matches.append(
                MatchRecord(
                    master_id=self._next_match_id(),
                    tmdb_index=tmdb_idx,
                    kaggle_index=kaggle_idx,
                    match_level="tmdb_id",
                )
            )

        return matches

    # --------------------------------------------------
    # IMDB ID
    # --------------------------------------------------
    def match_by_imdb_id(self, tmdb_movies, imdb_movies):

        matches = []

        imdb_index = {}

        for i, m in enumerate(imdb_movies):

            imdb_id = m.ids.imdb_id

            if imdb_id is not None:
                imdb_index[imdb_id] = (i, m)

        for tmdb_idx, tmdb in enumerate(tmdb_movies):

            imdb_id = tmdb.ids.imdb_id

            if imdb_id is None:
                continue

            if imdb_id not in imdb_index:
                continue

            imdb_idx, imdb = imdb_index[imdb_id]

            if normalize_title(tmdb.title) != normalize_title(imdb.title):
                continue

            matches.append(
                MatchRecord(
                    master_id=self._next_match_id(),
                    tmdb_index=tmdb_idx,
                    imdb_index=imdb_idx,
                    match_level="imdb_id",
                )
            )

        return matches