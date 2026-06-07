# processing/normalization/kaggle_normalizer.py

from typing import Dict, Any, List, Optional

from processing.normalization.base import BaseNormalizer
from processing.normalization.schema import (
    FilmNormalized,
    IDBlock,
    ScoreBlock,
    CastMember,
    ProductionBlock,
)


class KaggleNormalizer(BaseNormalizer):
    """
    Normaliseur Kaggle Movies.

    Objectif :
    - transformer dataset Kaggle en FilmNormalized
    - gérer genres (genre_names -> list)
    - sécuriser types
    - homogénéiser avec les autres sources
    """

    def _parse_genres(self, raw: Dict[str, Any]) -> List[str]:
        """
        Kaggle fournit souvent :
        - genre_names: "Horror, Thriller"
        """
        genre_str = raw.get("genre_names")

        if not genre_str or not isinstance(genre_str, str):
            return []

        return [g.strip() for g in genre_str.split(",") if g.strip()]

    def normalize(self, raw: Dict[str, Any]) -> FilmNormalized:

        # ----------------------------
        # IDS
        # ----------------------------
        ids = IDBlock(
            tmdb_id=raw.get("id"),
            imdb_id=raw.get("imdb_id"),
        )

        # ----------------------------
        # TITLES
        # ----------------------------
        title = raw.get("title")
        original_title = raw.get("original_title") or title

        # ----------------------------
        # DESCRIPTION
        # ----------------------------
        overview = raw.get("overview")

        # ----------------------------
        # TAGLINE
        # ----------------------------
        tagline = raw.get("tagline")

        # ----------------------------
        # GENRES (CORRIGÉ)
        # ----------------------------
        genres = self._parse_genres(raw)

        # ----------------------------
        # DATES
        # ----------------------------
        release_date = raw.get("release_date")
        release_year = raw.get("release_year")

        if release_date and not release_year:
            try:
                release_year = int(release_date[:4])
            except Exception:
                release_year = None

        # ----------------------------
        # RUNTIME
        # ----------------------------
        runtime_minutes = raw.get("runtime")
        if runtime_minutes is None:
            runtime_minutes = None

        # ----------------------------
        # SCORES
        # ----------------------------
        scores = ScoreBlock(
            tmdb=None,
            imdb=None,
            rotten_tomatoes=None,
            kaggle_vote_average=raw.get("vote_average"),
        )

        # ----------------------------
        # POPULARITY
        # ----------------------------
        popularity = raw.get("popularity")

        # ----------------------------
        # CAST (souvent vide côté Kaggle filtered)
        # ----------------------------
        cast = []

        # ----------------------------
        # CREW
        # ----------------------------
        crew_raw = raw.get("crew") or {}
        directors = crew_raw.get("directors") or []

        if isinstance(directors, str):
            directors = [directors]

        # ----------------------------
        # PRODUCTION
        # ----------------------------
        production = ProductionBlock(
            companies=raw.get("production_companies") or [],
            countries=raw.get("production_countries") or [],
            languages=raw.get("spoken_languages") or [],
        )

        # sécurisation types
        if not isinstance(production.companies, list):
            production.companies = []
        if not isinstance(production.countries, list):
            production.countries = []
        if not isinstance(production.languages, list):
            production.languages = []

        # ----------------------------
        # OUTPUT FINAL
        # ----------------------------
        return FilmNormalized(
            ids=ids,
            title=title,
            original_title=original_title,
            overview=overview,
            tagline=tagline,
            release_date=release_date,
            release_year=release_year,
            runtime_minutes=runtime_minutes,
            genres=genres,
            scores=scores,
            popularity=popularity,
            cast=cast,
            crew={"directors": directors},
            production=production,
            source={
                "tmdb": False,
                "imdb": False,
                "rotten": False,
                "kaggle": True,
            },
        )