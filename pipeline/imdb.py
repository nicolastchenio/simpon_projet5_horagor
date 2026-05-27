# pipeline/imdb.py

from ingestion.imdb_client import IMDbClient
from pathlib import Path
import json


class IMDbPipeline:
    """
    Pipeline d'ingestion IMDb SQLite.

    Responsabilités :
    - connexion à la base SQLite
    - extraction des films
    - sauvegarde des données brutes JSON
    """

    def __init__(
        self,
        db_path="data/raw/imdb/movie.sqlite",
        output_dir="data/raw/imdb"
    ):
        """
        Initialise le pipeline IMDb.
        """

        # Client SQLite IMDb
        self.client = IMDbClient(db_path)

        # Dossier de sortie des données brutes
        self.output_dir = Path(output_dir)

        # Création du dossier si inexistant
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def fetch_movies(self, limit: int = None):
        """
        Récupère les films depuis SQLite.

        Si limit=None :
        -> récupère tous les films.
        """

        query = "SELECT * FROM movies"

        # Limitation optionnelle
        if limit:
            query += f" LIMIT {limit}"

        self.client.cursor.execute(query)

        rows = self.client.cursor.fetchall()

        # Conversion sqlite Row -> dict
        return [dict(row) for row in rows]

    def enrich_movies(self, movies: list):
        """
        Enrichit les films avec les données directors.
        """

        enriched = []

        for movie in movies:

            director_id = movie.get("director_id")

            if not director_id:
                movie["director_name"] = None
                movie["director_gender"] = None
                movie["director_department"] = None
                enriched.append(movie)
                continue

            director = self.client.get_director_by_id(director_id)

            movie["director_name"] = director["name"] if director else None
            movie["director_gender"] = director["gender"] if director else None
            movie["director_department"] = director["department"] if director else None

            enriched.append(movie)

        return enriched

    def save_movies(self, movies: list):
        """
        Sauvegarde les films au format JSON brut.
        """

        output_file = self.output_dir / "imdb_movies.json"

        with open(output_file, "w", encoding="utf-8") as f:

            json.dump(
                movies,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(f"[OK] IMDb raw dataset saved -> {output_file}")

    def run(self, limit: int = None):
        """
        Exécute le pipeline complet IMDb.
        """

        print("\n=== DÉMARRAGE PIPELINE IMDb ===\n")

        # Extraction films
        movies = self.fetch_movies(limit=limit)
        
        enriched_movies = self.enrich_movies(movies)

        print(f"{len(movies)} films récupérés")

        # Sauvegarde JSON brut
        self.save_movies(enriched_movies)

        # Fermeture connexion SQLite
        self.client.close()

        print("\n=== PIPELINE IMDb TERMINÉ ===")