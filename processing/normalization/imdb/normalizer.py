# processing/normalization/imdb/normalizer.py

from typing import List, Dict, Any
from processing.normalization.utils import normalize_title, parse_iso_date, scale_score, extract_year

class IMDbNormalizer:
    """
    Normalisateur IMDb vers schéma Pivot.
    """

    def normalize_movie(self, movie: Dict[str, Any]) -> Dict[str, Any]:
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
            "runtime": None,
            "genres": ["Horror"],
            "overview": movie.get("overview"),
            "tagline": movie.get("tagline"),
            "score": scale_score(movie.get("vote_average")),
            "vote_count": movie.get("vote_count"),
            "popularity": movie.get("popularity"),
            "budget": movie.get("budget"),
            "revenue": movie.get("revenue"),
            "production_companies": [],
            "original_language": None,
            "director": movie.get("director_name"),
            "source": "imdb"
        }
        
        return normalized

    def normalize_dataset(self, movies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [self.normalize_movie(m) for m in movies]
