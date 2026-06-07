import json
from pathlib import Path

from processing.normalization.imdb_normalizer import IMDbNormalizer


def test_imdb_normalization():
    """
    Test d'intégration de la normalisation IMDb.

    Objectif :
    ----------
    - vérifier que le mapping IMDb → FilmNormalized fonctionne
    - produire un fichier JSON de sortie pour inspection visuelle
    - éviter qu'une erreur sur un film bloque tout le batch

    Flux :
    ------
    data/cleaned/imdb  →  IMDbNormalizer  →  data/normalized/imdb
    """

    # -----------------------------
    # 1. FICHIER SOURCE (IMDb cleaned)
    # -----------------------------
    input_file = Path("data/cleaned/imdb/cleaned_imdb_movies.json")

    # -----------------------------
    # 2. FICHIER DE SORTIE
    # -----------------------------
    output_file = Path("data/normalized/imdb/normalized_imdb.json")

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
    normalizer = IMDbNormalizer()

    normalized_movies = []

    # compteur de contrôle qualité
    success = 0
    fail = 0

    # -----------------------------
    # 5. NORMALISATION BATCH
    # -----------------------------
    for movie in raw_movies:

        try:
            # transformation IMDb → FilmNormalized
            normalized = normalizer.normalize(movie)

            # conversion Pydantic → dict JSON sérialisable
            normalized_movies.append(normalized.model_dump())

            success += 1

        except Exception as e:
            # ne bloque pas tout le pipeline si un film est mal formé
            print(f"[WARN] Film ignoré (id={movie.get('imdb_id')}): {e}")
            fail += 1

    # -----------------------------
    # 6. ÉCRITURE DU FICHIER NORMALISÉ
    # -----------------------------
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(normalized_movies, f, ensure_ascii=False, indent=2)

    # -----------------------------
    # 7. VALIDATION SIMPLE
    # -----------------------------
    print(f"[OK] Normalisation IMDb terminée -> {output_file}")
    print(f"[INFO] Succès={success} | Échecs={fail}")


# ---------------------------------------------------------
# Exécution directe (sans pytest)
# ---------------------------------------------------------
if __name__ == "__main__":
    test_imdb_normalization()