# processing/fusion/fuser.py

from typing import List, Dict, Any

class DataFuser:
    """
    Consolide les données de plusieurs sources selon une logique de priorité.
    Priorité : TMDB > Rotten > Kaggle > IMDb.
    """

    def __init__(self, priority_order: List[str] = ["rotten", "kaggle", "imdb"]):
        self.priority_order = priority_order

    def merge_movie(self, master_movie: Dict[str, Any], enrichment_data: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Fusionne un film maître avec ses correspondances.
        """
        # On part d'une copie du film TMDB
        merged = master_movie.copy()
        merged["enrichment_sources"] = []

        # Champs à potentiellement combler s'ils sont vides
        fields_to_fill = [
            "overview", "tagline", "runtime", "budget", "revenue", 
            "original_language", "production_companies", "genres", 
            "director", "cast", "poster_path"
        ]

        # Parcours des sources par priorité
        for source_name in self.priority_order:
            source_movie = enrichment_data.get(source_name)
            
            if not source_movie:
                continue

            merged["enrichment_sources"].append(source_name)

            # 1. Combler les trous
            for field in fields_to_fill:
                val = merged.get(field)
                source_val = source_movie.get(field)

                # Si le champ est vide dans le master, on prend la valeur de la source
                if val is None or val == "" or val == []:
                    if source_val is not None and source_val != "" and source_val != []:
                        merged[field] = source_val

            # 2. Agrégation des scores spécifiques
            if source_name == "rotten":
                merged["score_rotten_critics"] = source_movie.get("tomatometer")
                merged["score_rotten_audience"] = source_movie.get("popcornmeter")
                # Le score principal Rotten (average_rating) est déjà géré par la priorité si TMDB est vide
            elif source_name == "imdb":
                merged["score_imdb"] = source_movie.get("score")
                merged["vote_count_imdb"] = source_movie.get("vote_count")
            elif source_name == "kaggle":
                merged["score_kaggle"] = source_movie.get("score")

        return merged

    def fuse_datasets(self, mapping_table: List[Dict[str, Any]], datasets: Dict[str, Dict[any, Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Exécute la fusion sur l'ensemble du catalogue.
        datasets: {"tmdb": {id: movie}, "rotten": {id: movie}, ...}
        """
        fused_data = []

        for entry in mapping_table:
            tmdb_id = entry["tmdb_id"]
            master_movie = datasets["tmdb"].get(tmdb_id)

            if not master_movie:
                continue

            # Préparation des données d'enrichissement pour ce film
            enrichment_for_movie = {}
            for source_name in self.priority_order:
                source_id = entry["matches"].get(source_name)
                if source_id:
                    enrichment_for_movie[source_name] = datasets[source_name].get(source_id)

            # Fusion
            fused_movie = self.merge_movie(master_movie, enrichment_for_movie)
            fused_data.append(fused_movie)

        return fused_data
