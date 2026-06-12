# pipeline/tmdb.py

from ingestion.tmdb_client import TMDBClient
from pathlib import Path
import json
import time


class TMDBPipeline:
    """
    Pipeline d'ingestion TMDB pour les films Horror.

    Responsabilités :
    -----------------
    - récupérer les films Horror
    - enrichir chaque film avec ses détails complets
    - récupérer le casting principal
    - sauvegarder les datasets bruts enrichis

    IMPORTANT :
    Aucune transformation métier.
    Aucun nettoyage.
    Aucune normalisation.

    Le dataset produit est considéré comme du RAW enrichi.
    """

    def __init__(
        self,
        output_dir="data/raw/tmdb"
    ):
        """
        Initialisation du pipeline.
        """

        self.client = TMDBClient()

        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # ==================================================
    # DISCOVER HORROR MOVIES
    # ==================================================

    def fetch_page(
        self,
        page: int
    ):
        """
        Récupère une page de films Horror.
        """

        return self.client.get_horror_movies(
            page=page
        )

    # ==================================================
    # SAUVEGARDE PAGE BRUTE
    # ==================================================

    def save_page(
        self,
        data: dict,
        page: int
    ):
        """
        Sauvegarde une page brute.
        """

        file_path = (
            self.output_dir /
            f"horror_movies_page_{page}.json"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        return file_path

    # ==================================================
    # CASTING
    # ==================================================

    def build_cast(
        self,
        credits: dict,
        limit: int = 20
    ):
        """
        Construit une version simplifiée du casting.

        Exemple :

        [
            {
                "actor_id": 3810,
                "actor_name": "Javier Bardem",
                "character": "Max Cady"
            }
        ]
        """

        cast = []

        for actor in credits.get("cast", [])[:limit]:

            cast.append(
                {
                    "actor_id": actor.get("id"),
                    "actor_name": actor.get("name"),
                    "character": actor.get("character")
                }
            )

        return cast

    # ==================================================
    # ENRICHISSEMENT FILMS
    # ==================================================

    def enrich_movies(
        self,
        movies: list
    ):
        """
        Enrichit les films avec :

        - détails complets TMDB
        - casting principal
        """

        enriched_movies = []

        for movie in movies:

            movie_id = movie.get("id")

            print(
                f"Enrichissement film TMDB ID : {movie_id}"
            )

            try:

                # --------------------------------------
                # Détails complets du film
                # --------------------------------------

                details = (
                    self.client.get_movie_details(
                        movie_id
                    )
                )

                # --------------------------------------
                # Casting
                # --------------------------------------

                credits = (
                    self.client.get_movie_credits(
                        movie_id
                    )
                )

                cast = self.build_cast(
                    credits,
                    limit=20
                )

                # Ajout du casting
                details["cast"] = cast

                enriched_movies.append(
                    details
                )

            except Exception as e:

                print(
                    f"[ERREUR] Film {movie_id}"
                )

                print(e)

            # Respect du rate limit TMDB
            time.sleep(0.2)

        return enriched_movies

    # ==================================================
    # PIPELINE COMPLET
    # ==================================================

    def run(
        self,
        max_pages: int = 1
    ):
        """
        Exécute le pipeline complet.
        Si max_pages est None, récupère toutes les pages disponibles.
        """

        print(
            "=== Démarrage pipeline TMDB Horror ===\n"
        )

        current_page = 1
        
        while True:
            print(
                f"\nRécupération page {current_page}..."
            )

            # --------------------------------------
            # Discover Horror
            # --------------------------------------
            data = self.fetch_page(current_page)
            
            # Récupération du nombre total de pages au premier appel
            if current_page == 1:
                total_pages = data.get("total_pages", 1)
                
                # Si l'utilisateur a spécifié une limite, on la respecte
                if max_pages is not None:
                    limit_pages = min(max_pages, total_pages)
                else:
                    # Limite technique TMDB sur Discover (500 pages)
                    limit_pages = min(total_pages, 500)
                
                print(f"Total de pages disponibles : {total_pages}")
                print(f"Pages à traiter : {limit_pages}")

            movies = data.get(
                "results",
                []
            )

            print(
                f"{len(movies)} films récupérés (Page {current_page}/{limit_pages})"
            )

            # --------------------------------------
            # Enrichissement
            # --------------------------------------

            enriched_movies = (
                self.enrich_movies(
                    movies
                )
            )

            # --------------------------------------
            # Sauvegarde
            # --------------------------------------

            file_path = (
                self.output_dir /
                f"enriched_horror_page_{current_page}.json"
            )

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    enriched_movies,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            print(
                f"Dataset enrichi sauvegardé -> "
                f"{file_path}"
            )

            # Condition de sortie
            if current_page >= limit_pages:
                break
                
            current_page += 1

        print(
            "\n=== Pipeline TMDB terminé ==="
        )