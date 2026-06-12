# processing/normalization/rotten/normalizer.py

import re
from typing import List, Dict, Any
from datetime import datetime
from processing.normalization.utils import normalize_title, parse_iso_date, scale_score

class RottenNormalizer:
    """
    Normalisateur Rotten Tomatoes vers schéma Pivot.
    """

    def parse_runtime(self, runtime_str: str) -> int:
        """
        Convertit "1h 41m" en 101.
        """
        if not runtime_str or not isinstance(runtime_str, str):
            return None
        
        hours = 0
        minutes = 0
        
        h_match = re.search(r"(\d+)h", runtime_str)
        m_match = re.search(r"(\d+)m", runtime_str)
        
        if h_match:
            hours = int(h_match.group(1))
        if m_match:
            minutes = int(m_match.group(1))
            
        return hours * 60 + minutes

    def parse_rotten_date(self, date_str: str) -> str:
        """
        Convertit "Oct 26, 2015" en "2015-10-26".
        """
        if not date_str or not isinstance(date_str, str):
            return None
            
        try:
            # Essayer plusieurs formats courants sur RT
            for fmt in ("%b %d, %Y", "%Y-%m-%d"):
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime("%Y-%m-%d")
                except:
                    continue
            return parse_iso_date(date_str)
        except:
            return None

    def normalize_movie(self, movie: Dict[str, Any]) -> Dict[str, Any]:
        title = movie.get("title")
        release_date = self.parse_rotten_date(movie.get("release_date"))
        
        release_year = None
        if release_date:
            release_year = int(release_date[:4])

        # Extraction du casting simplifié
        cast_data = movie.get("cast")
        cast = []
        if isinstance(cast_data, list):
            for actor in cast_data:
                if isinstance(actor, dict) and "actor" in actor:
                    cast.append(actor["actor"])

        normalized = {
            "id": movie.get("url"), # URL comme ID technique
            "imdb_id": None,
            "title": title,
            "matching_title": normalize_title(title),
            "release_date": release_date,
            "release_year": release_year,
            "runtime": self.parse_runtime(movie.get("runtime")),
            "genres": movie.get("genre", []),
            "overview": movie.get("synopsis"),
            "tagline": None,
            # L'utilisateur demande que le score corresponde à average_rating
            "score": scale_score(movie.get("average_rating")), 
            "tomatometer": scale_score(movie.get("tomatometer")),
            "popcornmeter": scale_score(movie.get("popcornmeter")),
            "vote_count": None,
            "budget": None,
            "revenue": None,
            "director": movie.get("director", []), # Liste de réalisateurs
            "production_companies": movie.get("production_companies", []),
            "cast": cast,
            "original_language": movie.get("original_language"),
            "source": "rotten"
        }
        
        return normalized

    def normalize_dataset(self, movies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [self.normalize_movie(m) for m in movies]
