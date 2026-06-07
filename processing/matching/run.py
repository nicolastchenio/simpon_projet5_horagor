# processing/matching/run.py

from typing import List, Dict, Any

from processing.matching.id_matcher import IDMatcher
from processing.matching.fuzzy_matcher import FuzzyMatcher
from processing.matching.schema import MatchRecord


class MatchingPipeline:

    def __init__(self):
        self.id_matcher = IDMatcher()
        self.fuzzy_matcher = FuzzyMatcher()

    # --------------------------------------------------
    # ID MATCHING
    # --------------------------------------------------
    def apply_id_matching(
        self,
        tmdb: List[Dict[str, Any]],
        kaggle: List[Dict[str, Any]],
        imdb: List[Dict[str, Any]],
    ) -> List[MatchRecord]:

        results = []

        results += self.id_matcher.match_by_tmdb_id(tmdb, kaggle)
        results += self.id_matcher.match_by_imdb_id(tmdb, imdb)

        return results

    # --------------------------------------------------
    # FUZZY
    # --------------------------------------------------
    def apply_fuzzy_matching(
        self,
        tmdb: List[Dict[str, Any]],
        external: List[Dict[str, Any]],
        source: str,
    ) -> List[MatchRecord]:

        return self.fuzzy_matcher.match(tmdb, external, source)

    # --------------------------------------------------
    # RUN
    # --------------------------------------------------
    def run(self, tmdb, kaggle, imdb, rotten):

        master = {}

        # --------------------------------------------------
        # INITIALISATION MASTER
        # --------------------------------------------------
        for i in range(len(tmdb)):
            master[i] = MatchRecord(
                master_id=f"tmdb_{i}",
                tmdb_index=i,
                kaggle_index=None,
                imdb_index=None,
                rotten_index=None,
                match_level="MASTER",
            )

        # --------------------------------------------------
        # ID MATCHING (remplit master)
        # --------------------------------------------------
        id_matches = self.id_matcher.match_by_tmdb_id(tmdb, kaggle)

        for m in id_matches:
            if m.tmdb_index is not None:
                master[m.tmdb_index].kaggle_index = m.kaggle_index

        id_matches_imdb = self.id_matcher.match_by_imdb_id(tmdb, imdb)

        for m in id_matches_imdb:
            if m.tmdb_index is not None:
                master[m.tmdb_index].imdb_index = m.imdb_index

        # --------------------------------------------------
        # FUZZY MATCHING (complète uniquement les manquants)
        # --------------------------------------------------
        for i, m in enumerate(master.values()):

            # KAGGLE
            if m.kaggle_index is None:
                for j, k in enumerate(kaggle):
                    if self.fuzzy_matcher.is_match(tmdb[i], k):
                        m.kaggle_index = j
                        break

            # IMDB
            if m.imdb_index is None:
                for j, k in enumerate(imdb):
                    if self.fuzzy_matcher.is_match(tmdb[i], k):
                        m.imdb_index = j
                        break

            # ROTTEN
            if m.rotten_index is None:
                for j, k in enumerate(rotten):
                    if self.fuzzy_matcher.is_match(tmdb[i], k):
                        m.rotten_index = j
                        break

        return list(master.values())