# processing/cleaning/kaggle/cleaner.py

from typing import List, Dict, Any


class KaggleCleaner:
    """
    Nettoyage Kaggle strict.

    Objectif :
    ----------
    Transformer le dataset brut sélectionné
    en dataset propre sans normalisation.

    Ce cleaner :

    - supprime les espaces inutiles
    - transforme les chaînes vides en None
    - extrait release_year

    IMPORTANT :

    Aucune normalisation métier.
    Aucun mapping inter-sources.
    """

    def clean_string(
        self,
        value: Any
    ):
        """
        Nettoyage simple des chaînes.
        """

        if value is None:
            return None

        if not isinstance(value, str):
            return value

        value = value.strip()

        if value == "":
            return None

        return value

    def clean_movie(
        self,
        movie: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Nettoie un film.
        """

        cleaned = {

            # =====================
            # IDENTIFIANT
            # =====================
            "id": movie.get("id"),

            # =====================
            # TITRES
            # =====================
            "original_title": self.clean_string(
                movie.get("original_title")
            ),

            "title": self.clean_string(
                movie.get("title")
            ),

            # =====================
            # LANGUE
            # =====================
            "original_language": self.clean_string(
                movie.get("original_language")
            ),

            # =====================
            # DESCRIPTIONS
            # =====================
            "overview": self.clean_string(
                movie.get("overview")
            ),

            "tagline": self.clean_string(
                movie.get("tagline")
            ),

            # =====================
            # DATE
            # =====================
            "release_date": self.clean_string(
                movie.get("release_date")
            ),

            # =====================
            # POPULARITÉ
            # =====================
            "popularity": movie.get("popularity"),

            # =====================
            # VOTES
            # =====================
            "vote_count": movie.get("vote_count"),

            "vote_average": movie.get(
                "vote_average"
            ),

            # =====================
            # BUSINESS
            # =====================
            "budget": movie.get("budget"),

            "revenue": movie.get("revenue"),

            # =====================
            # DURÉE
            # =====================
            "runtime": movie.get("runtime"),

            # =====================
            # GENRES
            # =====================
            "genre_names": self.clean_string(
                movie.get("genre_names")
            ),

        }

        # =====================
        # RELEASE YEAR
        # =====================

        release_date = cleaned.get(
            "release_date"
        )

        if (
            release_date
            and isinstance(release_date, str)
            and len(release_date) >= 4
        ):
            try:

                cleaned["release_year"] = int(
                    release_date[:4]
                )

            except Exception:

                cleaned["release_year"] = None

        else:

            cleaned["release_year"] = None

        return cleaned

    def clean_dataset(
        self,
        movies: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Nettoie tout le dataset.
        """

        return [
            self.clean_movie(movie)
            for movie in movies
        ]