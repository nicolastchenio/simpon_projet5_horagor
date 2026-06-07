# processing/matching/run.py

from typing import List
from processing.matching.id_matcher import IDMatcher
from processing.matching.fuzzy_matcher import FuzzyMatcher
from processing.matching.schema import MatchRecord
from processing.normalization.schema import FilmNormalized


class MatchingPipeline:
    """
    Orchestrateur du matching multi-sources.
    
    Stratégie MDM :
    1. ID Matching (fort)
    2. Fuzzy Matching (fallback)
    
    Travaille EXCLUSIVEMENT sur FilmNormalized.
    """

    def __init__(self):
        self.id_matcher = IDMatcher()
        self.fuzzy_matcher = FuzzyMatcher()

    def run(
        self, 
        tmdb: List[FilmNormalized], 
        kaggle: List[FilmNormalized], 
        imdb: List[FilmNormalized], 
        rotten: List[FilmNormalized]
    ) -> List[MatchRecord]:
        """
        Exécute le matching complet entre TMDB (master) et les autres sources.
        """

        # Aggregator : tmdb_index -> MatchRecord
        aggregated = {}

        def get_or_create_record(tmdb_idx: int) -> MatchRecord:
            if tmdb_idx not in aggregated:
                aggregated[tmdb_idx] = MatchRecord(
                    master_id=f"match_{tmdb_idx:06d}",
                    tmdb_index=tmdb_idx
                )
            return aggregated[tmdb_idx]

        # On traite chaque source externe séparément
        sources = [
            ("kaggle", kaggle),
            ("imdb", imdb),
            ("rotten", rotten)
        ]

        for source_name, external_data in sources:
            if not external_data:
                continue

            matched_tmdb_indices = set()
            matched_external_indices = set()

            # --- 1. ID MATCHING (PRIORITAIRE) ---
            
            # Tentative via TMDB_ID
            id_matches = self.id_matcher.match_by_tmdb_id(tmdb, external_data, source_name)
            for m in id_matches:
                record = get_or_create_record(m.tmdb_index)
                record.source_indices.update(m.source_indices)
                record.match_level += f"[{m.match_level}]"
                matched_tmdb_indices.add(m.tmdb_index)
                matched_external_indices.add(m.source_indices[source_name])

            # Tentative via IMDB_ID (si pas encore matché par TMDB_ID)
            id_imdb_matches = self.id_matcher.match_by_imdb_id(tmdb, external_data, source_name)
            for m in id_imdb_matches:
                if m.tmdb_index in matched_tmdb_indices:
                    continue
                if m.source_indices[source_name] in matched_external_indices:
                    continue
                    
                record = get_or_create_record(m.tmdb_index)
                record.source_indices.update(m.source_indices)
                record.match_level += f"[{m.match_level}]"
                matched_tmdb_indices.add(m.tmdb_index)
                matched_external_indices.add(m.source_indices[source_name])

            # --- 2. FUZZY MATCHING (FALLBACK) ---
            
            # On ne tente le fuzzy que pour ce qui n'a pas été trouvé par ID
            remaining_tmdb = [
                (idx, film) for idx, film in enumerate(tmdb) 
                if idx not in matched_tmdb_indices
            ]
            remaining_external = [
                (idx, film) for idx, film in enumerate(external_data) 
                if idx not in matched_external_indices
            ]

            if not remaining_tmdb or not remaining_external:
                continue

            # Extraction des listes pour le fuzzy matcher
            tmdb_subset = [f for _, f in remaining_tmdb]
            ext_subset = [f for _, f in remaining_external]
            
            fuzzy_matches = self.fuzzy_matcher.match(tmdb_subset, ext_subset, source_name)
            
            for m in fuzzy_matches:
                # Récupération des vrais index originaux
                original_tmdb_idx = remaining_tmdb[m.tmdb_index][0]
                original_ext_idx = remaining_external[m.source_indices[source_name]][0]

                # Sécurité : un film TMDB ou externe ne doit pas être matché deux fois
                if original_tmdb_idx in matched_tmdb_indices:
                    continue
                if original_ext_idx in matched_external_indices:
                    continue

                record = get_or_create_record(original_tmdb_idx)
                record.source_indices[source_name] = original_ext_idx
                record.match_level += f"[{m.match_level}]"
                
                matched_tmdb_indices.add(original_tmdb_idx)
                matched_external_indices.add(original_ext_idx)

        return list(aggregated.values())
