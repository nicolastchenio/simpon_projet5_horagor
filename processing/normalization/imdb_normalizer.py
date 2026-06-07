# processing/normalization/imdb_normalizer.py

"""
IMDb Normalizer
----------------
Convertit les données IMDb (source brute) en FilmNormalized.

Rôle :
- standardiser la structure
- aligner avec le schéma commun du projet
- préparer le matching multi-sources
"""

from typing import Dict, Any, List, Optional

from processing.normalization.base import BaseNormalizer
from processing.normalization.schema import (
    FilmNormalized,
    IDBlock,
    ScoreBlock,
    CastMember,
    ProductionBlock,
)


class IMDbNormalizer(BaseNormalizer):
    """
    Normaliseur pour données IMDb.
    """

    def normalize(self, raw: Dict[str, Any]) -> FilmNormalized:
        """
        Transforme un film IMDb brut en FilmNormalized.
        """

        # ----------------------------
        # 1. IDENTIFIERS
        # ----------------------------

        raw_imdb_id = raw.get("imdb_id")

        ids = IDBlock(
            tmdb_id=None,  # pas utilisé ici
            imdb_id=str(raw_imdb_id) if raw_imdb_id is not None else None,
        )

        # ----------------------------
        # 2. TITLES
        # ----------------------------
        title = raw.get("title")
        original_title = raw.get("original_title") or raw.get("originalTitle")

        # ----------------------------
        # 3. DESCRIPTION
        # ----------------------------
        overview = raw.get("plot") or raw.get("overview")

        # ----------------------------
        # 4. RELEASE DATE / YEAR
        # ----------------------------
        release_date = raw.get("release_date") or raw.get("releaseDate")
        release_year = None
        if release_date:
            try:
                release_year = int(release_date[:4])
            except Exception:
                release_year = None

        # ----------------------------
        # 5. RUNTIME
        # ----------------------------
        runtime_minutes = raw.get("runtime") or raw.get("runtime_minutes")

        # ----------------------------
        # 6. GENRES
        # ----------------------------
        genres = raw.get("genres") or []

        # ----------------------------
        # 7. SCORES (IMDb uniquement ici)
        # ----------------------------
        scores = ScoreBlock(
            tmdb=None,
            imdb=raw.get("vote_average"),
            rotten_tomatoes=None,
            kaggle_vote_average=None,
        )

        # ----------------------------
        # 8. POPULARITY
        # ----------------------------
        popularity = raw.get("popularity")

        # ----------------------------
        # 9. CAST
        # ----------------------------
        cast_raw = raw.get("cast", [])
        cast = [
            CastMember(
                name=c.get("name"),
                character=c.get("character"),
            )
            for c in cast_raw
            if isinstance(c, dict)
        ]

        # ----------------------------
        # 10. PRODUCTION (IMDb souvent pauvre ici)
        # ----------------------------
        production = ProductionBlock(
            companies=[],
            countries=[],
            languages=[],
        )

        # ----------------------------
        # 11. OUTPUT FINAL
        # ----------------------------
        return FilmNormalized(
            ids=ids,
            title=title,
            original_title=original_title,
            overview=overview,
            tagline=raw.get("tagline"),
            release_date=release_date,
            release_year=release_year,
            runtime_minutes=runtime_minutes,
            genres=genres,
            scores=scores,
            popularity=popularity,
            cast=cast,
            crew={"directors": []},  # à améliorer plus tard
            production=production,
            source={
                "tmdb": False,
                "imdb": True,
                "rotten": False,
                "kaggle": False,
            },
        )