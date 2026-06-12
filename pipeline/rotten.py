# pipeline/rotten.py

from ingestion.rotten_client import RottenClient
from pathlib import Path
import json
import time


class RottenPipeline:
    """
    Pipeline RAW Rotten Tomatoes.

    Responsabilités :
    -----------------
    - récupérer plusieurs pages Rotten
    - fusionner les URLs uniques
    - enrichir les films (infos + scores + cast)
    - sauvegarder dataset brut + enrichi
    """

    BASES = {
        "movies_in_theaters": "movies_in_theaters",
        "movies_at_home": "movies_at_home",
        "movies_coming_soon": "movies_coming_soon",
        "movies_tv_shows": "tv_series_browse"
    }

    def __init__(self, output_dir="data/raw/rotten"):
        """
        Initialise le pipeline + client Selenium.
        """

        self.client = RottenClient()

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # =========================
    # SAUVEGARDE DATASET BRUT
    # =========================
    def save_dataset(self, base: str, urls: list):
        """
        Sauvegarde des URLs brutes (catalogue Rotten).
        """

        file_path = self.output_dir / f"{base}.json"

        data = {
            "base": base,
            "count": len(urls),
            "urls": urls
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"\nDataset sauvegardé : {file_path}")
        print(f"Total URLs : {len(urls)}")

        return file_path

    # =========================
    # PIPELINE PRINCIPAL
    # =========================
    def run(
        self,
        base: str,
        max_pages: int = 2,
        sleep_time: float = 1.0
    ):
        """
        Scrape plusieurs pages browse Rotten Tomatoes
        puis construit un dataset unique.
        """

        all_seen = set()
        previous_count = 0
        current_page = 1

        while True:
            # Condition de sortie si max_pages est défini
            if max_pages is not None and current_page > max_pages:
                break

            # construction URL browse (genre/sort fixés ici)
            url = self.client.build_browse_url(
                base=base,
                genre="horror",
                sort="a_z",
                page=current_page
            )

            print(f"\n===== PAGE {current_page} =====")
            print(f"URL : {url}")

            self.client.open_page(url)

            # attente simple chargement page
            time.sleep(sleep_time)

            html = self.client.get_html()

            # extraction liens films / séries
            movies = self.client.extract_movie_links(
                html,
                selector='a[data-qa="discovery-media-list-item-caption"]'
            )

            current_count = len(movies)

            print(f"URLs extraites : {current_count}")

            if not movies:
                print("STOP : aucune donnée")
                break

            # stop si pagination bloquée (RT duplique parfois les pages)
            # On vérifie si on a ajouté de nouveaux éléments
            initial_seen_count = len(all_seen)
            all_seen.update(movies)
            
            if len(all_seen) == initial_seen_count and current_page > 1:
                print("STOP : plus de nouveaux films trouvés (pagination stagnante)")
                break

            current_page += 1

        urls = sorted(all_seen)

        # sauvegarde brut
        self.save_dataset(base=base, urls=urls)

        # enrichissement
        enriched_movies = self.enrich_movies(urls)

        # sauvegarde enrichi
        self.save_enriched_dataset(base, enriched_movies)

        return urls

    # =========================
    # ENRICHISSEMENT FILMS
    # =========================
    def enrich_movies(self, urls: list):
        """
        Enrichit chaque film :
        - infos détaillées
        - scores RT
        - casting
        """

        enriched_movies = []

        for i, url in enumerate(urls, start=1):

            print(f"Enrichissement {i}/{len(urls)} : {url}")

            try:
                # =========================
                # PAGE FILM PRINCIPALE
                # =========================
                self.client.open_page(url)
                time.sleep(1)

                html = self.client.get_html()

                infos = self.client.extract_movie_infos(html)
                scores = self.client.extract_movie_scores(html)

                # =========================
                # PAGE CAST (ROUTE DÉDIÉE)
                # =========================
                cast_url = f"{url}/cast-and-crew"

                self.client.open_page(cast_url)

                time.sleep(2)

                cast_data = self.client.extract_movie_cast()        

                # =========================
                # FUSION FINAL
                # =========================
                movie_data = {
                    "url": url,
                    **infos,
                    **scores,
                    **cast_data
                }

                enriched_movies.append(movie_data)

            except Exception as e:

                print(f"[ERREUR] Scraping impossible : {url}")
                print(e)

        return enriched_movies

    # =========================
    # SAUVEGARDE ENRICHI
    # =========================
    def save_enriched_dataset(self, base: str, movies: list):
        """
        Sauvegarde dataset enrichi (films + scores + cast).
        """

        file_path = self.output_dir / f"{base}_enriched.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(movies, f, indent=4, ensure_ascii=False)

        print(f"\nDataset enrichi sauvegardé : {file_path}")

        return file_path

    # =========================
    # CLEAN EXIT
    # =========================
    def close(self):
        """
        Fermeture propre Selenium.
        """

        self.client.close()