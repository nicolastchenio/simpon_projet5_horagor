import json
from pathlib import Path

from processing.normalization.kaggle_normalizer import KaggleNormalizer


def test_kaggle_normalization():
    """
    Test d'intégration Kaggle → FilmNormalized

    Objectif :
    ----------
    - vérifier le mapping Kaggle
    - produire un fichier JSON exploitable
    - détecter les erreurs de normalisation
    """

    # -----------------------------
    # 1. INPUT FILE (Kaggle cleaned)
    # -----------------------------
    input_file = Path("data/cleaned/kaggle/cleaned_horror_movies_selected.json")

    # -----------------------------
    # 2. OUTPUT FILE
    # -----------------------------
    output_file = Path("data/normalized/kaggle/normalized_kaggle.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # 3. LOAD DATA
    # -----------------------------
    with open(input_file, "r", encoding="utf-8") as f:
        raw_movies = json.load(f)

    normalizer = KaggleNormalizer()

    normalized_movies = []

    success = 0
    errors = 0

    # -----------------------------
    # 4. NORMALIZATION LOOP
    # -----------------------------
    for movie in raw_movies:
        try:
            normalized = normalizer.normalize(movie)
            normalized_movies.append(normalized.model_dump())
            success += 1

        except Exception as e:
            errors += 1
            print(f"[ERROR] movie_id={movie.get('id')} -> {e}")

    # -----------------------------
    # 5. SAVE OUTPUT
    # -----------------------------
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(normalized_movies, f, ensure_ascii=False, indent=2)

    # -----------------------------
    # 6. SUMMARY
    # -----------------------------
    print(f"[OK] Kaggle normalization finished -> {output_file}")
    print(f"[INFO] Succès={success} | Échecs={errors}")


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    test_kaggle_normalization()