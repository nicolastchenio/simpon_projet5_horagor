# processing/normalization/base.py

from abc import ABC, abstractmethod
from typing import Dict, Any, List

from processing.normalization.schema import FilmNormalized


class BaseNormalizer(ABC):
    """
    Classe abstraite de normalisation.

    Objectif :
    ----------
    - définir une interface commune pour toutes les sources
    - garantir que chaque dataset implémente un mapping vers FilmNormalized
    """

    @abstractmethod
    def normalize(self, raw_data: Dict[str, Any]) -> FilmNormalized:
        """
        Convertit un objet brut (API / dataset / fichier JSON)
        en objet standardisé FilmNormalized.
        """
        pass

    def safe_get(self, data: Dict[str, Any], key: str, default=None):
        """
        Helper générique :
        - évite les KeyError
        - centralise la logique de fallback
        """
        return data.get(key, default)

    def clean_list(self, value: Any) -> List:
        """
        Nettoie les listes :
        - gère None
        - force type list
        """
        if value is None:
            return []
        if isinstance(value, list):
            return value
        return [value]