# processing/normalization/kaggle/normalizer.py

from typing import List, Dict, Any
from processing.normalization.utils import normalize_title, parse_iso_date, scale_score

class KaggleNormalizer:
    """
    Normalisateur Kaggle vers schéma Pivot.
    """

    def normalize_movie(self, movie: Dict[str, Any]) -> Dict[str, Any]:
        title = movie.get("title")
        
        # Genres : "Horror, Thriller" -> ["Horror", "Thriller"]
        genres = []
        raw_genres = movie.get("genre_names")
        if raw_genres:
            genres = [g.strip() for g in raw_genres.split(",")]

        normalized = {
            "id": movie.get("id"),
            "imdb_id": None,
            "title": title,
            "matching_title": normalize_title(title),
            "release_date": parse_iso_date(movie.get("release_date")),
            "release_year": movie.get("release_year"),
            "runtime": movie.get("runtime"),
            "genres": genres,
            "overview": movie.get("overview"),
            "tagline": movie.get("tagline"),
            "score": scale_score(movie.get("vote_average")),
            "vote_count": movie.get("vote_count"),
            "budget": movie.get("budget"),
            "revenue": movie.get("revenue"),
            "production_companies": [],
            "original_language": movie.get("original_language"),
            "source": "kaggle"
        }
        
        return normalized

    def normalize_dataset(self, movies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [self.normalize_movie(m) for m in movies]
