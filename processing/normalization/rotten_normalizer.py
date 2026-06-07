# processing/normalization/rotten_normalizer.py

from typing import Dict, Any, List, Optional
import re

from processing.normalization.base import BaseNormalizer
from processing.normalization.schema import (
    FilmNormalized,
    IDBlock,
    ScoreBlock,
    CastMember,
    ProductionBlock,
)


class RottenNormalizer(BaseNormalizer):
    """
    Normaliseur des données Rotten Tomatoes (scraping multi-pages).

    Objectif :
    - transformer les données HTML scrapées en structure FilmNormalized
    - homogénéiser avec TMDB / IMDb
    - sécuriser les types (string, float, list)
    """

    # =========================================================
    # CONVERSION RUNTIME : "1h 50m" → 110 minutes
    # =========================================================
    def _parse_runtime(self, runtime: str) -> Optional[int]:
        if not runtime:
            return None

        match = re.search(r"(?:(\d+)h)?\s*(?:(\d+)m)?", runtime)
        if not match:
            return None

        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0

        total = hours * 60 + minutes
        return total if total > 0 else None

    # =========================================================
    # CONVERSION "89%" → 89.0
    # =========================================================
    def _parse_percent(self, value: Any) -> Optional[float]:
        if value is None:
            return None

        try:
            return float(str(value).replace("%", "").strip())
        except Exception:
            return None

    # =========================================================
    # CONVERSION SAFE FLOAT
    # =========================================================
    def _parse_float(self, value: Any) -> Optional[float]:
        try:
            return float(value)
        except Exception:
            return None

    # =========================================================
    # NORMALISATION PRINCIPALE
    # =========================================================
    def normalize(self, raw: Dict[str, Any]) -> FilmNormalized:

        # ----------------------------
        # IDENTIFIANTS (non disponibles sur Rotten)
        # ----------------------------
        ids = IDBlock(
            tmdb_id=None,
            imdb_id=None,
        )

        # ----------------------------
        # TITRES / DESCRIPTION
        # ----------------------------
        title = raw.get("title")
        overview = raw.get("synopsis")

        # fallback sécurité
        original_title = raw.get("original_title") or title

        # ----------------------------
        # GENRES
        # ----------------------------
        genres = raw.get("genre") or []
        if not isinstance(genres, list):
            genres = []

        # ----------------------------
        # DATE / ANNÉE
        # ----------------------------
        release_date_raw = raw.get("release_date")

        release_date = release_date_raw
        release_year = None

        if isinstance(release_date_raw, str):
            match = re.search(r"(\d{4})", release_date_raw)
            if match:
                release_year = int(match.group(1))

        # ----------------------------
        # DUREE
        # ----------------------------
        runtime_minutes = self._parse_runtime(raw.get("runtime"))

        # ----------------------------
        # SCORES
        # ----------------------------
        scores = ScoreBlock(
            tmdb=None,
            imdb=self._parse_float(raw.get("average_rating")),
            rotten_tomatoes=self._parse_percent(raw.get("tomatometer")),
            kaggle_vote_average=None,
        )

        # ----------------------------
        # CAST
        # ----------------------------
        cast_raw = raw.get("cast") or []
        cast: List[CastMember] = [
            CastMember(
                name=c.get("actor"),
                character=c.get("character"),
            )
            for c in cast_raw
            if isinstance(c, dict)
        ]

        # ----------------------------
        # PRODUCTION
        # ----------------------------
        companies = raw.get("production_companies") or []
        if not isinstance(companies, list):
            companies = []

        production = ProductionBlock(
            companies=companies,
            countries=[],
            languages=[],
        )

        # ----------------------------
        # CREW (réalisateurs)
        # ----------------------------
        directors = raw.get("director") or []

        # sécurisation si string unique
        if isinstance(directors, str):
            directors = [directors]

        # ----------------------------
        # OUTPUT FINAL STANDARDISÉ
        # ----------------------------
        return FilmNormalized(
            ids=ids,
            title=title,
            original_title=original_title,
            overview=overview,
            tagline=None,
            release_date=release_date,
            release_year=release_year,
            runtime_minutes=runtime_minutes,
            genres=genres,
            scores=scores,
            popularity=None,
            cast=cast,
            crew={"directors": directors},
            production=production,
            source={
                "tmdb": False,
                "imdb": False,
                "rotten": True,
                "kaggle": False,
            },
        )