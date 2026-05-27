# processing/cleaning/imdb/cleaner.py

from typing import List, Dict, Any
from datetime import datetime


class IMDBCLeaner:
    """
    Nettoyage IMDb (SQL → dataset propre)

    Objectif :
    - harmoniser structure avec TMDB cleaned
    - préparer normalisation multi-sources
    - supprimer incohérences
    """

    def clean_movie(self, movie: Dict[str, Any]) -> Dict[str, Any]:

        cleaned = {
            # IDENTIFIANTS
            "id": movie.get("id"),
            "imdb_id": movie.get("uid"),  # équivalent externe IMDb
            "tmdb_id": None,

            # TITRES
            "title": movie.get("title"),
            "original_title": movie.get("original_title"),

            # TEXTE RAG
            "overview": movie.get("overview") or "",
            "tagline": movie.get("tagline") or "",

            # GENRES (IMDb ne les fournit pas ici → placeholder)
            "genres": [],

            # DATES
            "release_date": movie.get("release_date"),
            "release_year": None,

            # FEATURES NUMÉRIQUES
            "runtime": None,
            "vote_average": movie.get("vote_average"),
            "vote_count": movie.get("vote_count"),
            "popularity": movie.get("popularity"),

            # ENRICHISSEMENT DIRECTOR (déjà présent)
            "director_id": movie.get("director_id"),
            "director_name": movie.get("director_name"),
            "director_gender": movie.get("director_gender"),
            "director_department": movie.get("director_department"),

            # BUSINESS
            "budget": movie.get("budget"),
            "revenue": movie.get("revenue"),

            # MÉTADONNÉES
            "source": "imdb"
        }

        # -----------------------------
        # release_year extraction
        # -----------------------------
        try:
            if cleaned["release_date"]:
                cleaned["release_year"] = datetime.strptime(
                    cleaned["release_date"], "%Y-%m-%d"
                ).year
        except Exception:
            cleaned["release_year"] = None

        return cleaned

    def clean_dataset(self, movies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Nettoie une liste de films IMDb
        """
        return [self.clean_movie(m) for m in movies]