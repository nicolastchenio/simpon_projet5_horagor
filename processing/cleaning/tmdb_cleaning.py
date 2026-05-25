# processing/cleaning/tmdb_cleaning.py

from typing import List, Dict, Any
from datetime import datetime


class TMDBCleaner:
    """
    Nettoyage strict TMDB selon schéma canonique projet.
    Objectif : garantir un dataset homogène pour RAG + matching + fusion.
    """

    def clean_movie(self, movie: Dict[str, Any]) -> Dict[str, Any]:

        # -----------------------------
        # 1. STRUCTURE CIBLE FIXE
        # -----------------------------
        cleaned = {
            # CORE DATA (MDM + RAG)
            "id": movie.get("id"),
            "imdb_id": movie.get("imdb_id"),
            "title": movie.get("title"),
            "original_title": movie.get("original_title"),
            "overview": movie.get("overview") or "",
            "tagline": movie.get("tagline") or "",

            # LISTES NORMALISÉES
            "genres": [],
            "release_date": movie.get("release_date"),
            "release_year": None,
            "runtime": movie.get("runtime"),
            "vote_average": movie.get("vote_average"),
            "popularity": movie.get("popularity"),

            # ENRICHISSEMENT
            "budget": movie.get("budget"),
            "revenue": movie.get("revenue"),
            "production_companies": [],
            "production_countries": [],
            "original_language": movie.get("original_language"),
            "spoken_languages": [],
            "status": movie.get("status"),
        }

        # -----------------------------
        # 2. GENRES
        # -----------------------------
        for g in movie.get("genres", []):
            if isinstance(g, dict) and g.get("name"):
                cleaned["genres"].append(g["name"])

        # -----------------------------
        # 3. PRODUCTION COMPANIES
        # -----------------------------
        for c in movie.get("production_companies", []):
            if isinstance(c, dict) and c.get("name"):
                cleaned["production_companies"].append(c["name"])

        # -----------------------------
        # 4. PRODUCTION COUNTRIES
        # -----------------------------
        for c in movie.get("production_countries", []):
            if isinstance(c, dict) and c.get("name"):
                cleaned["production_countries"].append(c["name"])

        # -----------------------------
        # 5. SPOKEN LANGUAGES
        # -----------------------------
        for l in movie.get("spoken_languages", []):
            if isinstance(l, dict) and l.get("english_name"):
                cleaned["spoken_languages"].append(l["english_name"])

        # -----------------------------
        # 6. RELEASE YEAR (MDM + FILTER)
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
        return [self.clean_movie(m) for m in movies]