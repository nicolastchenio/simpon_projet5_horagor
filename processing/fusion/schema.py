# processing/fusion/schema.py

from pydantic import BaseModel
from typing import Optional, List


class UnifiedFilm(BaseModel):
    """
    Représentation finale d’un film après fusion MDM.
    """

    master_id: str

    # identifiants multi-sources
    tmdb_id: Optional[int] = None
    imdb_id: Optional[str] = None
    kaggle_index: Optional[int] = None
    rotten_index: Optional[int] = None

    # données principales fusionnées
    title: str
    release_date: Optional[str] = None
    overview: Optional[str] = None
    tagline: Optional[str] = None
    runtime_minutes: Optional[int] = None
    genres: List[str] = []

    # enrichissement
    sources: List[str] = []

    # trace du matching
    confidence: float = 1.0