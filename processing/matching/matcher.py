# processing/matching/matcher.py

import json
from pathlib import Path
from difflib import SequenceMatcher
from typing import List, Dict, Any

class MovieMatcher:
    """
    Moteur de matching inter-sources.
    
    Logique :
    1. Correspondance exacte sur (matching_title, release_year).
    2. Si échec, Fuzzy matching sur title (Seuil > 0.85) pour la même année.
    """

    def __init__(self, threshold: float = 0.85):
        self.threshold = threshold

    def similar(self, a: str, b: str) -> float:
        """Calcule le score de similitude entre deux chaînes."""
        return SequenceMatcher(None, a, b).ratio()

    def find_match(self, target_movie: Dict[str, Any], source_dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Cherche un match pour un film cible dans un dataset source.
        """
        target_title = target_movie.get("matching_title")
        target_year = target_movie.get("release_year")

        if not target_title or target_year is None:
            return None

        # --- ÉTAPE 1 : MATCH EXACT ---
        for movie in source_dataset:
            if movie.get("matching_title") == target_title and movie.get("release_year") == target_year:
                return movie

        # --- ÉTAPE 2 : FUZZY MATCHING (sur la même année) ---
        best_match = None
        best_score = 0

        for movie in source_dataset:
            if movie.get("release_year") == target_year:
                score = self.similar(target_title, movie.get("matching_title", ""))
                if score > self.threshold and score > best_score:
                    best_score = score
                    best_match = movie

        return best_match

    def create_mapping(self, master_data: List[Dict[str, Any]], sources: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Crée la table de correspondance en prenant TMDB comme base.
        """
        mapping_table = []

        print(f"Starting matching for {len(master_data)} master movies...")

        for tmdb_movie in master_data:
            entry = {
                "tmdb_id": tmdb_movie.get("id"),
                "title": tmdb_movie.get("title"),
                "release_year": tmdb_movie.get("release_year"),
                "matches": {
                    "tmdb": tmdb_movie.get("id"),
                    "rotten": None,
                    "kaggle": None,
                    "imdb": None
                }
            }

            # On cherche dans chaque source d'enrichissement
            for source_name, dataset in sources.items():
                match = self.find_match(tmdb_movie, dataset)
                if match:
                    entry["matches"][source_name] = match.get("id")
            
            mapping_table.append(entry)

        return mapping_table
