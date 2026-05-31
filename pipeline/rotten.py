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
    - sauvegarder un JSON unique par dataset

    Exemple :

    data/raw/rotten/
        movies_at_home.json
        movies_in_theaters.json
        movies_coming_soon.json
        tv_series_browse.json
    """

    BASES = {
        "movies_in_theaters": "movies_in_theaters",
        "movies_at_home": "movies_at_home",
        "movies_coming_soon": "movies_coming_soon",
        "movies_tv_shows": "tv_series_browse"
    }

    def __init__(self, output_dir="data/raw/rotten"):
        """
        Initialise le pipeline.
        """

        self.client = RottenClient()

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def save_dataset(self, base: str, urls: list):
        """
        Sauvegarde le dataset complet d'une catégorie.
        """

        file_path = self.output_dir / f"{base}.json"

        data = {
            "base": base,
            "count": len(urls),
            "urls": urls
        }

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

        print(f"\nDataset sauvegardé : {file_path}")
        print(f"Total URLs : {len(urls)}")

        return file_path

    def run(
        self,
        base: str,
        max_pages: int = 2,
        sleep_time: float = 1.0
    ):
        """
        Scrape plusieurs pages Rotten
        puis construit un dataset unique.
        """

        all_seen = set()
        previous_count = 0

        for page in range(1, max_pages + 1):

            url = self.client.build_browse_url(
                base=base,
                genre="horror",
                sort="a_z",
                page=page
            )

            print(f"\n===== PAGE {page} =====")
            print(f"URL : {url}")

            self.client.open_page(url)

            time.sleep(sleep_time)

            html = self.client.get_html()

            movies = self.client.extract_movie_links(
                html,
                selector='a[data-qa="discovery-media-list-item-caption"]'
            )

            current_count = len(movies)

            print(f"URLs extraites : {current_count}")

            if not movies:
                print("STOP : aucune donnée")
                break

            # Rotten renvoie parfois :
            # page1=28
            # page2=56
            # page3=84
            #
            # Si le nombre n'augmente plus,
            # inutile de continuer.

            if current_count == previous_count:
                print("STOP : plus aucune nouvelle donnée")
                break

            previous_count = current_count

            all_seen.update(movies)

        urls = sorted(all_seen)

        self.save_dataset(
            base=base,
            urls=urls
        )
 
        # enrichissement
        enriched_movies = self.enrich_movies(
            urls
        )

        # sauvegarde enrichie
        self.save_enriched_dataset(
            base,
            enriched_movies
        )
           
        return urls

    def enrich_movies(self, urls: list):
        """
        Enrichit les URLs Rotten Tomatoes avec
        les informations détaillées des fiches films/séries.
        """

        enriched_movies = []

        for i, url in enumerate(urls, start=1):

            print(
                f"Enrichissement {i}/{len(urls)} : {url}"
            )

            try:

                # ouverture fiche film
                self.client.open_page(url)

                time.sleep(1)

                html = self.client.get_html()

                # infos film
                infos = self.client.extract_movie_infos(html)

                # scores Rotten
                scores = self.client.extract_movie_scores(html)

                # fusion
                movie_data = {
                    "url": url,
                    **infos,
                    **scores
                }

                enriched_movies.append(movie_data)

            except Exception as e:

                print(
                    f"[ERREUR] Impossible de scraper : {url}"
                )

                print(e)

        return enriched_movies

    def save_enriched_dataset(
        self,
        base: str,
        movies: list
    ):
        """
        Sauvegarde le dataset enrichi.
        """

        file_path = (
            self.output_dir /
            f"{base}_enriched.json"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                movies,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"\nDataset enrichi sauvegardé : {file_path}"
        )

        return file_path

    def close(self):
        """
        Fermeture Selenium.
        """

        self.client.close()