# processing/gold/generator.py

from typing import List, Dict, Any

class GoldGenerator:
    """
    Génère le dataset "Gold" final.
    
    Logique :
    - Filtrage des films sans description.
    - Calcul du score global "HorRAGor".
    - Sélection stricte des colonnes métier (sans IDs techniques).
    """

    def calculate_global_score(self, movie: Dict[str, Any]) -> float:
        """
        Calcule la moyenne des scores disponibles.
        """
        scores = []
        
        # Récupération des différents scores possibles
        s_tmdb = movie.get("score") # Score TMDB (normalisé à 10)
        s_rotten_critics = movie.get("score_rotten_critics")
        s_rotten_audience = movie.get("score_rotten_audience")
        s_imdb = movie.get("score_imdb")
        s_kaggle = movie.get("score_kaggle")
        
        for s in [s_tmdb, s_rotten_critics, s_rotten_audience, s_imdb, s_kaggle]:
            if s is not None:
                scores.append(s)
        
        if not scores:
            return None
            
        return round(sum(scores) / len(scores), 1)

    def generate_gold_movie(self, movie: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transforme un film fusionné en film Gold.
        """
        
        # 1. Calcul du score global
        score_horragor = self.calculate_global_score(movie)
        
        # 2. Construction de l'objet Gold (colonnes métier uniquement)
        gold = {
            "title": movie.get("title"),
            "release_year": movie.get("release_year"),
            "original_language": movie.get("original_language"),
            "overview": movie.get("overview"),
            "tagline": movie.get("tagline"),
            "genres": movie.get("genres", []),
            "director": movie.get("director"), # Peut être une liste ou str selon la source
            "cast": movie.get("cast", []),
            "runtime": movie.get("runtime"),
            "budget": movie.get("budget"),
            "revenue": movie.get("revenue"),
            "production_companies": movie.get("production_companies", []),
            "score_tmdb": movie.get("score"),
            "score_imdb": movie.get("score_imdb"),
            "score_rotten_critics": movie.get("score_rotten_critics"),
            "score_rotten_audience": movie.get("score_rotten_audience"),
            "score_horragor": score_horragor
        }
        
        return gold

    def is_valid_for_gold(self, movie: Dict[str, Any]) -> bool:
        """
        Critères d'inclusion dans le dataset Gold.
        """
        overview = movie.get("overview")
        tagline = movie.get("tagline")
        
        # On garde le film s'il a au moins une description ou une tagline
        if not overview and not tagline:
            return False
            
        return True

    def process(self, merged_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Exécute la transformation Gold.
        """
        gold_data = []
        
        for movie in merged_data:
            if self.is_valid_for_gold(movie):
                gold_movie = self.generate_gold_movie(movie)
                gold_data.append(gold_movie)
                
        return gold_data
