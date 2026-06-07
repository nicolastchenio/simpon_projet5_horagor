# processing/fusion/merger.py

from typing import List, Dict
from collections import defaultdict

from processing.fusion.schema import UnifiedFilm
from processing.matching.schema import MatchRecord
from processing.normalization.schema import FilmNormalized


class FusionEngine:
    """
    Fusion des MatchRecords en entités finales.
    """

    def __init__(self):
        self.counter = 0

    def _next_id(self):
        self.counter += 1
        return f"film_{self.counter:06d}"

    # --------------------------------------------------
    # BUILD INDEX
    # --------------------------------------------------
    def build_groups(self, matches: List[MatchRecord]) -> Dict[int, List[MatchRecord]]:
        """
        Regroupe tous les MatchRecords par TMDB index (master)
        """

        groups = defaultdict(list)

        for m in matches:
            groups[m.tmdb_index].append(m)

        return groups

    # --------------------------------------------------
    # FUSION D’UN GROUPE
    # --------------------------------------------------
    def merge_group(
        self, 
        group: List[MatchRecord], 
        tmdb_data: List[FilmNormalized],
        kaggle_data: List[FilmNormalized] = None,
        imdb_data: List[FilmNormalized] = None,
        rotten_data: List[FilmNormalized] = None
    ) -> UnifiedFilm:
        """
        Fusionne un groupe de matches en une entité unique enrichie.
        Priorité : TMDB > Rotten > Kaggle > IMDb
        """

        match_record = group[0]
        tmdb_item = tmdb_data[match_record.tmdb_index]

        # 1. Initialisation avec la source maître (TMDB)
        unified = UnifiedFilm(
            master_id=self._next_id(),
            tmdb_id=tmdb_item.ids.tmdb_id,
            imdb_id=tmdb_item.ids.imdb_id,
            title=tmdb_item.title,
            release_date=tmdb_item.release_date,
            sources=["tmdb"],
        )

        # Préparation des données d'enrichissement disponibles
        enrichment_sources = []

        # Ordre de priorité : Rotten (1), Kaggle (2), IMDb (3)
        if "rotten" in match_record.source_indices and rotten_data:
            enrichment_sources.append(("rotten", rotten_data[match_record.source_indices["rotten"]]))
        if "kaggle" in match_record.source_indices and kaggle_data:
            enrichment_sources.append(("kaggle", kaggle_data[match_record.source_indices["kaggle"]]))
        if "imdb" in match_record.source_indices and imdb_data:
            enrichment_sources.append(("imdb", imdb_data[match_record.source_indices["imdb"]]))

        # Champs à enrichir (en plus des IDs/Index déjà gérés)
        current_overview = tmdb_item.overview
        current_tagline = tmdb_item.tagline
        current_runtime = tmdb_item.runtime_minutes
        current_genres = set(tmdb_item.genres or [])

        # 2. Enrichissement itératif selon priorité
        for source_name, source_item in enrichment_sources:
            unified.sources.append(source_name)

            # Synopsis (Overview)
            if not current_overview and source_item.overview:
                current_overview = source_item.overview

            # Tagline
            if not current_tagline and source_item.tagline:
                current_tagline = source_item.tagline

            # Runtime
            if not current_runtime and source_item.runtime_minutes:
                current_runtime = source_item.runtime_minutes

            # Genres (Union des genres)
            if source_item.genres:
                current_genres.update(source_item.genres)

            # Indexation spécifique
            if source_name == "kaggle":
                unified.kaggle_index = match_record.source_indices["kaggle"]
            elif source_name == "rotten":
                unified.rotten_index = match_record.source_indices["rotten"]

        # 3. Finalisation des données enrichies
        unified.sources = list(set(unified.sources))
        unified.overview = current_overview
        unified.tagline = current_tagline
        unified.runtime_minutes = current_runtime
        unified.genres = list(current_genres)

        return unified

    # --------------------------------------------------
    # PIPELINE COMPLET
    # --------------------------------------------------
    def merge(
        self, 
        matches: List[MatchRecord], 
        tmdb_data: List[FilmNormalized],
        kaggle_data: List[FilmNormalized] = None,
        imdb_data: List[FilmNormalized] = None,
        rotten_data: List[FilmNormalized] = None
    ) -> List[UnifiedFilm]:

        groups = self.build_groups(matches)
        results = []

        for _, group in groups.items():
            results.append(
                self.merge_group(
                    group, 
                    tmdb_data, 
                    kaggle_data, 
                    imdb_data, 
                    rotten_data
                )
            )

        return results