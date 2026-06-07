import json
from pathlib import Path

from processing.normalization.rotten_normalizer import RottenNormalizer


def test_rotten_normalization():
    """
    Test d'intégration du RottenNormalizer.

    Objectif :
    ----------
    - vérifier la transformation Rotten → FilmNormalized
    - gérer plusieurs sources Rotten (theaters, at_home, coming_soon, tv_series)
    - produire un fichier JSON exploitable pour inspection

    Flux :
    ------
    data/cleaned/rotten → RottenNormalizer → data/normalized/rotten
    """

    # -----------------------------
    # 1. DOSSIER SOURCE
    # -----------------------------
    input_dir = Path("data/cleaned/rotten")

    # -----------------------------
    # 2. DOSSIER OUTPUT
    # -----------------------------
    output_dir = Path("data/normalized/rotten")
    output_dir.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # 3. INITIALISATION NORMALIZER
    # -----------------------------
    normalizer = RottenNormalizer()

    normalized_movies = []
    success = 0
    errors = 0

    # -----------------------------
    # 4. LOOP SUR TOUS LES FICHIERS
    # -----------------------------
    for file in input_dir.glob("*.json"):

        with open(file, "r", encoding="utf-8") as f:
            raw_movies = json.load(f)

        for movie in raw_movies:
            try:
                normalized = normalizer.normalize(movie)
                normalized_movies.append(normalized.model_dump())
                success += 1

            except Exception as e:
                errors += 1
                print(f"[ERROR] {file.name} -> {e}")

    # -----------------------------
    # 5. OUTPUT JSON
    # -----------------------------
    output_file = output_dir / "normalized_rotten.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(normalized_movies, f, ensure_ascii=False, indent=2)

    # -----------------------------
    # 6. RESULTATS
    # -----------------------------
    print(f"[OK] Rotten normalization finished -> {output_file}")
    print(f"[INFO] Succès={success} | Échecs={errors}")


# ---------------------------------------------------------
# Exécution directe
# ---------------------------------------------------------
if __name__ == "__main__":
    test_rotten_normalization()