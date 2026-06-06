# processing/cleaning/tmdb/cleaner.py

from typing import List, Dict, Any


class TMDBCleaner:
    """
    Nettoyage TMDB.

    Responsabilités :
    - nettoyage texte
    - suppression espaces inutiles
    - gestion NULL
    - nettoyage listes
    - suppression doublons
    - filtrage Horror
    """

    def clean_string(self, value: Any):
        """
        Nettoie une chaîne :
        - strip espaces
        - normalisation basique
        """

        if value is None:
            return None

        if not isinstance(value, str):
            return value

        return value.strip()

    def clean_list(self, values: Any) -> list:
        """
        Nettoie une liste :
        - supprime None
        - supprime strings vides
        - supprime doublons
        - nettoie strings
        """

        if values is None:
            return []

        cleaned = []
        seen = set()

        for value in values:

            # nettoyage string
            if isinstance(value, str):
                value = value.strip()
                if value == "":
                    continue

            # skip None
            if value is None:
                continue

            # suppression doublons
            key = str(value)

            if key not in seen:
                seen.add(key)
                cleaned.append(value)

        return cleaned

    def clean_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Nettoyage récursif des dictionnaires imbriqués.
        """

        cleaned = {}

        for key, value in data.items():

            # string
            if isinstance(value, str):
                cleaned[key] = self.clean_string(value)

            # liste
            elif isinstance(value, list):
                cleaned[key] = self.clean_list(value)

            # dict imbriqué (IMPORTANT pour genres, production_companies, etc.)
            elif isinstance(value, dict):
                cleaned[key] = self.clean_dict(value)

            else:
                cleaned[key] = value

        return cleaned

    def clean_movie(self, movie: Dict[str, Any]) -> Dict[str, Any]:
        """
        Nettoie un film TMDB sans modifier sa structure.
        """

        return self.clean_dict(movie)

    def is_horror(self, movie: Dict[str, Any]) -> bool:
        """
        Vérifie si le film est de type Horror / Horreur.
        Robuste (case + strip).
        """

        genres = movie.get("genres", [])

        for genre in genres:

            if isinstance(genre, dict):
                name = genre.get("name")

                if isinstance(name, str):
                    name = name.strip().lower()

                    if name in ["horror", "horreur"]:
                        return True

        return False

    def clean_dataset(self, movies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Nettoyage complet + filtrage Horror.
        """

        cleaned_movies = []

        for movie in movies:

            cleaned_movie = self.clean_movie(movie)

            if self.is_horror(cleaned_movie):
                cleaned_movies.append(cleaned_movie)

        return cleaned_movies