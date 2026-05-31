# processing/cleaning/rotten/cleaner.py

from typing import List, Dict, Any


class RottenCleaner:
    """
    Cleaner Rotten Tomatoes.

    Responsabilités :
    -----------------
    - nettoyage des chaînes de caractères
    - suppression des espaces inutiles
    - nettoyage des listes
    - suppression des doublons dans les listes
    - gestion des valeurs NULL
    - filtrage des contenus Horror

    Important :
    -----------
    Ce cleaner ne normalise PAS les données.
    Il conserve la structure d'origine Rotten.
    """

    def clean_string(self, value):
        """
        Nettoie une chaîne de caractères.
        """
        if value is None:
            return None

        if not isinstance(value, str):
            return value

        return value.strip()

    def clean_list(self, values):
        """
        Nettoie une liste :
        - suppression des valeurs vides
        - suppression des espaces
        - suppression des doublons
        """
        if values is None:
            return None

        cleaned = []

        for value in values:

            if not value:
                continue

            value = str(value).strip()

            if value and value not in cleaned:
                cleaned.append(value)

        return cleaned

    def clean_movie(self, movie: Dict[str, Any]):
        """
        Nettoie un film Rotten Tomatoes.
        Aucun renommage de colonne.
        Aucune transformation métier.
        """

        cleaned = {

            # URL Rotten
            "url": self.clean_string(movie.get("url")),

            # TITRE DU FILM
            "title": self.clean_string(movie.get("title")),

            # Résumé du film
            "synopsis": self.clean_string(movie.get("synopsis")),

            # Réalisateurs
            "director": self.clean_list(movie.get("director")),

            # Producteurs
            "producer": self.clean_list(movie.get("producer")),

            # Scénaristes
            "screenwriter": self.clean_list(movie.get("screenwriter")),

            # Distributeur
            "distributor": self.clean_string(movie.get("distributor")),

            # Sociétés de production
            "production_companies": self.clean_list(movie.get("production_companies")),

            # Classification
            "rating": self.clean_string(movie.get("rating")),

            # Genres
            "genre": self.clean_list(movie.get("genre")),

            # Langue originale
            "original_language": self.clean_string(movie.get("original_language")),

            # Date de sortie brute
            "release_date": self.clean_string(movie.get("release_date")),

            # Box office
            "box_office": self.clean_string(movie.get("box_office")),

            # Runtime
            "runtime": self.clean_string(movie.get("runtime")),

            # Sound mix
            "sound_mix": self.clean_list(movie.get("sound_mix")),

            # Aspect ratio
            "aspect_ratio": self.clean_string(movie.get("aspect_ratio")),

            # Scores Rotten
            "tomatometer": self.clean_string(movie.get("tomatometer")),
            "popcornmeter": self.clean_string(movie.get("popcornmeter")),
            "average_rating": self.clean_string(movie.get("average_rating")),
            "sentiment": self.clean_string(movie.get("sentiment"))
        }

        return cleaned

    def is_horror(self, movie: Dict[str, Any]):
        """
        Filtre Horror uniquement.
        """
        genres = movie.get("genre")

        if not genres:
            return False

        return "Horror" in genres

    def clean_dataset(self, movies: List[Dict[str, Any]]):
        """
        Nettoyage complet dataset.
        """
        cleaned_movies = []

        for movie in movies:

            cleaned_movie = self.clean_movie(movie)

            if self.is_horror(cleaned_movie):
                cleaned_movies.append(cleaned_movie)

        return cleaned_movies