# tests/normalization/test_tmdb_normalization.py

import json
from pathlib import Path

from processing.normalization.tmdb_normalizer import TMDBNormalizer


def test_tmdb_normalization():
    """
    Test d'intégration de la normalisation TMDB.

    Objectif :
    ----------
    - vérifier que le mapping TMDB → FilmNormalized fonctionne
    - produire un fichier JSON de sortie pour inspection visuelle
    """

    # -----------------------------
    # 1. FICHIER SOURCE (cleaned TMDB)
    # -----------------------------
    input_file = Path("data/cleaned/tmdb/cleaned_enriched_horror_page_1.json")

    # -----------------------------
    # 2. FICHIER DE SORTIE (normalized TMDB)
    # -----------------------------
    output_file = Path("data/normalized/tmdb/normalized_horror_page_1.json")

    # création dossier si nécessaire
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # 3. CHARGEMENT DES DONNÉES BRUTES
    # -----------------------------
    with open(input_file, "r", encoding="utf-8") as f:
        raw_movies = json.load(f)

    # -----------------------------
    # 4. INITIALISATION DU NORMALIZER
    # -----------------------------
    normalizer = TMDBNormalizer()

    normalized_movies = []

    # -----------------------------
    # 5. NORMALISATION BATCH
    # -----------------------------
    for movie in raw_movies:
        # transformation vers FilmNormalized
        normalized = normalizer.normalize(movie)

        # conversion Pydantic → dict JSON serialisable
        normalized_movies.append(normalized.model_dump())

    # -----------------------------
    # 6. ÉCRITURE DU FICHIER NORMALISÉ
    # -----------------------------
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(normalized_movies, f, ensure_ascii=False, indent=2)

    # message de validation
    print(f"[OK] Normalisation TMDB terminée -> {output_file}")


# ---------------------------------------------------------
# Permet d'exécuter le fichier directement sans pytest
# ---------------------------------------------------------
if __name__ == "__main__":
    test_tmdb_normalization()