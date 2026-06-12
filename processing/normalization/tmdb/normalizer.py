# processing/normalization/tmdb/normalizer.py

from typing import List, Dict, Any
from processing.normalization.utils import normalize_title, parse_iso_date, scale_score, extract_year

class TMDBNormalizer:
    """
    Normalisateur TMDB vers schéma Pivot.
    """

    def normalize_movie(self, movie: Dict[str, Any]) -> Dict[str, Any]:
        # Extraction des genres (liste de dict -> liste de str)
        genres = []
        for g in movie.get("genres", []):
            if isinstance(g, dict) and "name" in g:
                genres.append(g["name"])
            elif isinstance(g, str):
                genres.append(g)

        # Extraction des compagnies
        companies = []
        for c in movie.get("production_companies", []):
            if isinstance(c, dict) and "name" in c:
                companies.append(c["name"])
            elif isinstance(c, str):
                companies.append(c)

        # Extraction du casting simplifié
        cast = []
        for actor in movie.get("cast", []):
            if isinstance(actor, dict) and "actor_name" in actor:
                cast.append(actor["actor_name"])

        title = movie.get("title")
        release_date = parse_iso_date(movie.get("release_date"))
        
        # Priorité au release_year déjà présent, sinon extraction depuis la date
        release_year = movie.get("release_year")
        if release_year is None and release_date:
            release_year = extract_year(release_date)
        
        normalized = {
            "id": movie.get("id"),
            "imdb_id": movie.get("imdb_id"),
            "title": title,
            "matching_title": normalize_title(title),
            "release_date": release_date,
            "release_year": release_year,
            "runtime": movie.get("runtime"),
            "genres": genres,
            "overview": movie.get("overview"),
            "tagline": movie.get("tagline"),
            "score": scale_score(movie.get("vote_average")),
            "vote_count": movie.get("vote_count"),
            "popularity": movie.get("popularity"),
            "poster_path": movie.get("poster_path"),
            "budget": movie.get("budget"),
            "revenue": movie.get("revenue"),
            "production_companies": companies,
            "cast": cast,
            "original_language": movie.get("original_language"),
            "source": "tmdb"
        }
        
        return normalized

    def normalize_dataset(self, movies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [self.normalize_movie(m) for m in movies]
