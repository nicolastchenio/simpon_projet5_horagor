# processing/normalization/tmdb_normalizer.py

from typing import Dict, Any

from processing.normalization.base import BaseNormalizer
from processing.normalization.schema import (
    FilmNormalized,
    IDBlock,
    ScoreBlock,
    ProductionBlock,
    CastMember,
    CrewBlock
)


class TMDBNormalizer(BaseNormalizer):
    """
    Normaliseur pour les données TMDB.

    Responsabilités :
    -----------------
    - extraction des champs TMDB
    - conversion vers FilmNormalized
    - nettoyage des structures imbriquées (cast, genres, production)
    """

    def normalize(self, raw_data: Dict[str, Any]) -> FilmNormalized:
        """
        Convertit un film TMDB brut en FilmNormalized.
        """

        # -----------------------------
        # IDENTIFIANTS
        # -----------------------------
        ids = IDBlock(
            tmdb_id=raw_data.get("id"),
            imdb_id=raw_data.get("imdb_id")
        )

        # -----------------------------
        # GENRES
        # TMDB: [{"id": 27, "name": "Horreur"}, ...]
        # -----------------------------
        genres = [
            g.get("name")
            for g in raw_data.get("genres", [])
            if isinstance(g, dict)
        ]

        # -----------------------------
        # CAST
        # -----------------------------
        cast = [
            CastMember(
                name=member.get("actor_name"),
                character=member.get("character")
            )
            for member in raw_data.get("cast", [])
            if isinstance(member, dict)
        ]

        # -----------------------------
        # PRODUCTION COMPANIES
        # -----------------------------
        companies = [
            c.get("name")
            for c in raw_data.get("production_companies", [])
            if isinstance(c, dict)
        ]

        # -----------------------------
        # COUNTRIES
        # -----------------------------
        countries = [
            c.get("name")
            for c in raw_data.get("production_countries", [])
            if isinstance(c, dict)
        ]

        # -----------------------------
        # LANGUAGES
        # -----------------------------
        languages = [
            l.get("english_name")
            for l in raw_data.get("spoken_languages", [])
            if isinstance(l, dict)
        ]

        # -----------------------------
        # CREW (TMDB ici minimal)
        # -----------------------------
        crew = CrewBlock(
            directors=[]  # TMDB ne fournit pas directement dans ton dataset
        )

        # -----------------------------
        # SCORES
        # -----------------------------
        scores = ScoreBlock(
            tmdb=raw_data.get("vote_average"),
            imdb=None,
            rotten_tomatoes=None,
            kaggle_vote_average=None
        )

        # -----------------------------
        # FILM NORMALISÉ FINAL
        # -----------------------------
        return FilmNormalized(
            ids=ids,

            title=raw_data.get("title"),
            original_title=raw_data.get("original_title"),

            overview=raw_data.get("overview"),
            tagline=raw_data.get("tagline"),

            release_date=raw_data.get("release_date"),
            runtime_minutes=raw_data.get("runtime"),

            genres=genres,

            scores=scores,

            popularity=raw_data.get("popularity"),

            cast=cast,

            crew=crew,

            production=ProductionBlock(
                companies=companies,
                countries=countries,
                languages=languages
            ),

            source={
                "tmdb": True,
                "imdb": False,
                "rotten": False,
                "kaggle": False
            }
        )