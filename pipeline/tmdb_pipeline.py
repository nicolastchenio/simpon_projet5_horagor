from ingestion.tmdb_client import TMDBClient
from pathlib import Path
import json
import time


class TMDBPipeline:
    """
    Pipeline d'ingestion TMDB pour les films Horror.
    Responsable de la récupération et du stockage des données brutes.
    """

    def __init__(self, output_dir="data/raw/tmdb"):
        self.client = TMDBClient()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def fetch_page(self, page: int):
        """
        Récupère une page de films Horror depuis TMDB.
        """
        return self.client.get_horror_movies(page=page)

    def save_page(self, data: dict, page: int):
        """
        Sauvegarde une page de résultats en JSON.
        """
        file_path = self.output_dir / f"horror_movies_page_{page}.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return file_path

    def enrich_movies(self, movies: list):
        """
        Enrichit les films avec les détails complets TMDB.
        """

        enriched_movies = []

        for movie in movies:

            movie_id = movie.get("id")

            print(f"Enrichissement film TMDB ID : {movie_id}")

            # Récupération des détails complets
            details = self.client.get_movie_details(movie_id)

            enriched_movies.append(details)

            # Petite pause API
            time.sleep(0.2)

        return enriched_movies
    
    def run(self, max_pages: int = 1):
        """
        Exécute le pipeline TMDB enrichi.
        """

        print("=== Démarrage pipeline TMDB Horror ===\n")

        for page in range(1, max_pages + 1):

            print(f"\nRécupération page {page}...")

            # Discover movies
            data = self.fetch_page(page)

            movies = data.get("results", [])

            print(f"{len(movies)} films récupérés")

            # Enrichissement détaillé
            enriched_movies = self.enrich_movies(movies)

            # Sauvegarde
            file_path = self.output_dir / f"enriched_horror_page_{page}.json"

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(
                    enriched_movies,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            print(f"Dataset enrichi sauvegardé -> {file_path}")

        print("\n=== Pipeline TMDB terminé ===")