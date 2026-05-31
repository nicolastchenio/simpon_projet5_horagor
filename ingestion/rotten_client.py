import time
import json
from typing import Optional, List, Dict

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class RottenClient:
    """
    Client technique Selenium pour Rotten Tomatoes.

    RESPONSABILITÉ :
    ----------------
    Ce client NE contient AUCUNE logique métier.

    Il fournit uniquement :
    - navigation navigateur (Selenium)
    - récupération HTML
    - parsing générique (BeautifulSoup)
    - extraction réutilisable (catalogue, infos, scores)

    La logique métier (genre, tri, pagination, dataset) doit être
    gérée dans les tests ou pipelines.
    """

    BASE_URL = "https://www.rottentomatoes.com"

    # =========================
    # INITIALISATION SELENIUM
    # =========================

    def __init__(self):
        # Ouverture navigateur Chrome
        self.driver = webdriver.Chrome()

        # WebDriverWait (utile pour futurs waits JS)
        self.wait = WebDriverWait(self.driver, 10)

    def open_homepage(self):
        """Ouvre la page d'accueil Rotten Tomatoes."""
        self.driver.get(self.BASE_URL)

    def open_page(self, url: str):
        """Ouvre une URL arbitraire."""
        self.driver.get(url)

    def get_html(self) -> str:
        """Retourne le HTML rendu (DOM final après JS)."""
        return self.driver.page_source

    def get_page_title(self):
        """Retourne le titre de la page."""
        return self.driver.title

    def close(self):
        """Ferme proprement le navigateur."""
        self.driver.quit()

    # =========================
    # OUTILS
    # =========================

    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Centralisation BeautifulSoup.

        Permet d’éviter duplication du parsing HTML.
        """
        return BeautifulSoup(html, "html.parser")

    def build_browse_url(
        self,
        base: str,
        genre: Optional[str],
        sort: Optional[str],
        page: int
    ) -> str:
        """
        Construit une URL Rotten Tomatoes (niveau technique uniquement).

        Ce n’est PAS de la logique métier :
        - juste assemblage d’URL
        - aucun choix de contenu
        """

        url = f"{self.BASE_URL}/browse/{base}/"

        params = []

        if genre:
            params.append(f"genres:{genre}")

        if sort:
            params.append(f"sort:{sort}")

        if params:
            url += "~".join(params)

        if page > 1:
            url += f"?page={page}"

        return url


    # =========================
    # CATALOGUE FILMS (GÉNÉRIQUE)
    # =========================
    def extract_movie_links(
        self,
        html: str,
        selector: str,
        base_url=None
    ):
        """
        Extrait les URLs des films et séries TV depuis une page catalogue.

        Args:
            html: code HTML de la page à analyser.
            selector: sélecteur CSS permettant de cibler les liens
                    contenant les fiches Rotten Tomatoes.
            base_url: URL de base à utiliser pour construire les URLs
                    complètes. Si None, utilise self.BASE_URL.

        Returns:
            Liste des URLs complètes des films (/m/)
            et séries TV (/tv/).
        """

        # Transformation du HTML en objet BeautifulSoup
        # pour faciliter les recherches dans le DOM.
        soup = self.parse_html(html)

        # Utilise l'URL fournie ou l'URL Rotten Tomatoes par défaut.
        base = base_url or self.BASE_URL

        # Liste qui contiendra les URLs trouvées.
        movies = []

        # Parcourt tous les éléments correspondant au sélecteur CSS.
        for link in soup.select(selector):

            # Récupère la valeur de l'attribut href.
            href = link.get("href")

            # Ignore les balises sans href.
            if not href:
                continue

            # Ne conserve que les liens vers :
            # - les films (/m/)
            # - les séries TV (/tv/)
            if href.startswith("/m/") or href.startswith("/tv/"):

                # Construit une URL absolue puis l'ajoute à la liste.
                movies.append(base + href)

        # Retourne toutes les URLs collectées.
        return movies



    def get_movie_links_paginated(
        self,
        base: str,
        selector: str,
        genre: Optional[str] = None,
        sort: Optional[str] = None,
        max_pages: Optional[int] = None,
        sleep_time: float = 1.5
    ) -> List[str]:
        """
        Pagination générique Rotten Tomatoes.

        Le test fournit :
        - base
        - genre
        - sort

        Le client :
        - construit URL
        - scrape
        - pagine
        """

        all_movies = set()
        previous_page = None
        page = 1

        while True:

            if max_pages and page > max_pages:
                break

            url = self.build_browse_url(
                base=base,
                genre=genre,
                sort=sort,
                page=page
            )

            try:
                self.open_page(url)
                time.sleep(sleep_time)
            except Exception:
                break

            html = self.get_html()
            movies = self.extract_movie_links(html, selector)

            if not movies:
                break

            if movies == previous_page:
                break

            previous_page = movies
            all_movies.update(movies)

            page += 1

        return list(all_movies)

    # =========================
    # MOVIE DETAILS (MOVIE INFO)
    # =========================

    def extract_movie_infos(self, html: str) -> Dict:
        """
        Extraction des informations détaillées d’un film
        (Movie Info section Rotten Tomatoes).
        """

        soup = self.parse_html(html)

        # =========================
        # STRUCTURE DE BASE
        # =========================
        result = {
            "title": None,
            "synopsis": None,
            "director": None,
            "producer": None,
            "screenwriter": None,
            "distributor": None,
            "production_companies": None,
            "rating": None,
            "genre": None,
            "original_language": None,
            "release_date": None,
            "box_office": None,
            "runtime": None,
            "sound_mix": None,
            "aspect_ratio": None,
        }

        # =========================
        # TITLE (IMPORTANT)
        # =========================
        try:
            title_element = self.driver.find_element(
                "css selector",
                'rt-text[slot="title"]'
            )

            result["title"] = title_element.text.strip() if title_element.text else None

        except Exception:
            result["title"] = None

        # =========================
        # SYNOPSIS
        # =========================
        synopsis = soup.select_one('[data-qa="synopsis-value"]')
        if synopsis:
            result["synopsis"] = synopsis.get_text(strip=True)

        # =========================
        # MOVIE INFO BLOCKS
        # =========================
        items = soup.select('[data-qa="item"]')

        for item in items:
            label = item.select_one('[data-qa="item-label"]')
            values = item.select('[data-qa="item-value"]')

            if not label:
                continue

            key = label.get_text(strip=True)
            vals = [v.get_text(strip=True) for v in values]

            if key == "Director":
                result["director"] = vals
            elif key == "Producer":
                result["producer"] = vals
            elif key == "Screenwriter":
                result["screenwriter"] = vals
            elif key == "Distributor":
                result["distributor"] = vals[0] if vals else None
            elif key == "Production Co":
                result["production_companies"] = vals
            elif key == "Rating":
                result["rating"] = vals[0] if vals else None
            elif key == "Genre":
                result["genre"] = vals
            elif key == "Original Language":
                result["original_language"] = vals[0] if vals else None
            elif key == "Release Date (Theaters)":
                result["release_date"] = vals[0] if vals else None
            elif key == "Box Office (Gross USA)":
                result["box_office"] = vals[0] if vals else None
            elif key == "Runtime":
                result["runtime"] = vals[0] if vals else None
            elif key == "Sound Mix":
                result["sound_mix"] = vals
            elif key == "Aspect Ratio":
                result["aspect_ratio"] = vals[0] if vals else None

        return result

    # =========================
    # SCORES (TOMATOMETER / AUDIENCE)
    # =========================

    def extract_movie_scores(self, html: str) -> Dict:
        """
        Extraction des scores Rotten Tomatoes.

        Sources :
        - Tomatometer (critics)
        - Popcornmeter (audience)
        - sentiment
        """

        soup = self.parse_html(html)

        result = {
            "tomatometer": None,
            "popcornmeter": None,
            "average_rating": None,
            "sentiment": None,
        }

        script = soup.find("script", {"id": "media-scorecard-json"})

        if script and script.string:
            data = json.loads(script.string)

            critics = data.get("criticsScore", {})
            audience = data.get("audienceScore", {})

            result["tomatometer"] = critics.get("scorePercent")
            result["popcornmeter"] = audience.get("scorePercent")
            result["average_rating"] = audience.get("averageRating")
            result["sentiment"] = critics.get("sentiment")

        return result