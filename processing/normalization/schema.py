# processing/normalization/schema.py

from pydantic import BaseModel
from typing import List, Optional, Dict


# =========================
# IDENTIFIANTS MULTI-SOURCES
# =========================
class IDBlock(BaseModel):
    # Identifiant TMDB (source principale)
    tmdb_id: Optional[int] = None

    # Identifiant IMDb (peut être absent ou non fiable au début)
    imdb_id: Optional[str] = None


# =========================
# GENRES NORMALISÉS
# =========================
class GenreBlock(BaseModel):
    # Liste normalisée de genres (toujours en list[str])
    genres: List[str] = []


# =========================
# SCORES MULTI-SOURCES
# =========================
class ScoreBlock(BaseModel):
    # Score TMDB (0–10)
    tmdb: Optional[float] = None

    # Score IMDb (0–10)
    imdb: Optional[float] = None

    # Score Rotten Tomatoes (0–100)
    rotten_tomatoes: Optional[float] = None

    # Score Kaggle (0–10)
    kaggle_vote_average: Optional[float] = None


# =========================
# PRODUCTION / MÉTADONNÉES
# =========================
class ProductionBlock(BaseModel):
    # Sociétés de production
    companies: List[str] = []

    # Pays de production
    countries: List[str] = []

    # Langues du film
    languages: List[str] = []


# =========================
# CAST UNIFIÉ
# =========================
class CastMember(BaseModel):
    # Nom de l’acteur
    name: str

    # Rôle joué (peut être absent selon source)
    character: Optional[str] = None


# =========================
# CREW (ÉQUIPE TECHNIQUE)
# =========================
class CrewBlock(BaseModel):
    # Liste des réalisateurs
    directors: List[str] = []


# =========================
# SCHÉMA PRINCIPAL UNIFIÉ
# =========================
class FilmNormalized(BaseModel):

    # =====================
    # IDENTIFIANTS
    # =====================
    ids: IDBlock

    # =====================
    # INFORMATIONS PRINCIPALES
    # =====================
    title: str
    original_title: Optional[str] = None

    overview: Optional[str] = None
    tagline: Optional[str] = None

    # =====================
    # TEMPS / CHRONOLOGIE
    # =====================
    release_date: Optional[str] = None  # format ISO 8601 obligatoire
    release_year: Optional[int] = None

    # durée en minutes (normalisation obligatoire)
    runtime_minutes: Optional[int] = None

    # =====================
    # GENRES
    # =====================
    genres: List[str] = []

    # =====================
    # SCORES
    # =====================
    scores: ScoreBlock = ScoreBlock()

    # =====================
    # POPULARITÉ (TMDB surtout)
    # =====================
    popularity: Optional[float] = None

    # =====================
    # DONNÉES STRUCTURÉES
    # =====================
    cast: List[CastMember] = []

    crew: CrewBlock = CrewBlock()

    production: ProductionBlock = ProductionBlock()

    # =====================
    # TRAÇABILITÉ SOURCES
    # =====================
    source: Dict[str, bool] = {}