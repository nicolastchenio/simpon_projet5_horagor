# processing/matching/id_matcher.py

from typing import List
from processing.matching.schema import MatchRecord
from processing.matching.utils import normalize_title
from processing.normalization.schema import FilmNormalized


class IDMatcher:
    """
    Matching basé sur identifiants :
    - tmdb_id
    - imdb_id

    Travaille EXCLUSIVEMENT sur FilmNormalized.
    """

    def __init__(self):
        self.counter = 0

    def _next_match_id(self) -> str:
        self.counter += 1
        return f"id_{self.counter:06d}"

    def match_by_tmdb_id(
        self,
        tmdb_movies: List[FilmNormalized],
        external_movies: List[FilmNormalized],
        source_name: str = "kaggle"
    ) -> List[MatchRecord]:

        matches = []
        ext_index = {}

        for i, movie in enumerate(external_movies):
            tmdb_id = movie.ids.tmdb_id
            if tmdb_id is not None:
                ext_index[tmdb_id] = i

        for tmdb_idx, tmdb in enumerate(tmdb_movies):
            tmdb_id = tmdb.ids.tmdb_id
            if tmdb_id is not None and tmdb_id in ext_index:
                ext_idx = ext_index[tmdb_id]

                # Double vérification sur le titre
                if normalize_title(tmdb.title) == normalize_title(external_movies[ext_idx].title):
                    matches.append(
                        MatchRecord(
                            master_id=self._next_match_id(),
                            tmdb_index=tmdb_idx,
                            source_indices={source_name: ext_idx},
                            match_level=f"ID_TMDB_{source_name.upper()}"
                        )
                    )

        return matches

    def match_by_imdb_id(
        self,
        tmdb_movies: List[FilmNormalized],
        external_movies: List[FilmNormalized],
        source_name: str = "imdb"
    ) -> List[MatchRecord]:

        matches = []
        ext_index = {}

        for i, movie in enumerate(external_movies):
            imdb_id = movie.ids.imdb_id
            if imdb_id is not None:
                ext_index[imdb_id] = i

        for tmdb_idx, tmdb in enumerate(tmdb_movies):
            imdb_id = tmdb.ids.imdb_id
            if imdb_id is not None and imdb_id in ext_index:
                ext_idx = ext_index[imdb_id]

                if normalize_title(tmdb.title) == normalize_title(external_movies[ext_idx].title):
                    matches.append(
                        MatchRecord(
                            master_id=self._next_match_id(),
                            tmdb_index=tmdb_idx,
                            source_indices={source_name: ext_idx},
                            match_level=f"ID_IMDB_{source_name.upper()}"
                        )
                    )

        return matches