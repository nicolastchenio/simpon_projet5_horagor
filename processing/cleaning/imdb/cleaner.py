# processing/cleaning/imdb/cleaner.py

from typing import List, Dict, Any
from datetime import datetime


class IMDBCLeaner:
    """
    Nettoyage IMDb strict (source brute → propre)

    Objectif :
    - supprimer bruit
    - sécuriser types
    - extraire champs simples
    - aucune logique de normalisation inter-sources
    """

    def clean_movie(self, movie: Dict[str, Any]) -> Dict[str, Any]:

        cleaned = {
            # IDENTIFIANTS
            "id": movie.get("id"),
            "imdb_id": movie.get("uid"),

            # TITRES
            "title": movie.get("title"),
            "original_title": movie.get("original_title"),

            # TEXTES
            "overview": movie.get("overview") or None,
            "tagline": movie.get("tagline") or None,

            # GENRES (on ne transforme rien → brut si absent)
            "genres": movie.get("genres"),

            # DATES
            "release_date": movie.get("release_date"),

            # FEATURES NUMÉRIQUES (clean uniquement = cast safe)
            "runtime": movie.get("runtime"),
            "budget": movie.get("budget"),
            "revenue": movie.get("revenue"),
            "popularity": movie.get("popularity"),
            "vote_average": movie.get("vote_average"),
            "vote_count": movie.get("vote_count"),

            # DIRECTOR (si déjà présent en base IMDb)
            "director_id": movie.get("director_id"),
            "director_name": movie.get("director_name"),
            "director_gender": movie.get("director_gender"),
            "director_department": movie.get("director_department"),

            # META
            "source": "imdb"
        }

        # -----------------------------
        # release_year (simple extraction, pas de normalisation métier)
        # -----------------------------
        release_date = cleaned.get("release_date")
        if release_date and isinstance(release_date, str) and len(release_date) >= 4:
            try:
                cleaned["release_year"] = int(release_date[:4])
            except Exception:
                cleaned["release_year"] = None
        else:
            cleaned["release_year"] = None

        return cleaned

    def clean_dataset(self, movies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [self.clean_movie(m) for m in movies]