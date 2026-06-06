import polars as pl
from ingestion.kaggle_client import KaggleClient


def test_kaggle_pipeline_filters():
    """
    Test du pipeline de filtres Kaggle.

    Objectif :
    - valider les filtres métier simples (genre, notes, revenus)
    - vérifier la cohérence des sous-ensembles
    - préparer la base pour exploitation analytique
    """

    # =========================
    # CHARGEMENT DATASET
    # =========================
    client = KaggleClient("data/raw/kaggle/horror_movies.csv")
    df = client.load_dataset()

    print("\n===================================")
    print("     PIPELINE FILTERS TEST")
    print("===================================\n")

    # =========================
    # 1. OVERVIEW
    # =========================
    print("=== DATASET OVERVIEW ===")
    print(f"Lignes : {df.height}")
    print(f"Colonnes : {df.width}")

    # =========================
    # 2. FILTRE : FILMS HORROR UNIQUEMENT
    # =========================
    horror_df = df.filter(
        pl.col("genre_names").str.contains("Horror", literal=False)
    )

    print("\n=== HORROR FILTER ===")
    print(f"Films Horror : {horror_df.height}")

    assert horror_df.height > 0, "Aucun film Horror détecté"

    # =========================
    # 3. FILTRE : FILMS BIEN NOTÉS
    # =========================
    high_rated_df = df.filter(
        pl.col("vote_average") >= 7
    )

    print("\n=== HIGH RATED FILTER (>=7) ===")
    print(f"Films bien notés : {high_rated_df.height}")

    assert high_rated_df.height > 0, "Aucun film bien noté"

    # =========================
    # 4. FILTRE : FILMS RENTABLES
    # =========================
    profitable_df = df.filter(
        (pl.col("revenue") > pl.col("budget")) &
        (pl.col("budget") > 0)
    )

    print("\n=== PROFITABLE FILTER ===")
    print(f"Films rentables : {profitable_df.height}")

    assert profitable_df.height > 0, "Aucun film rentable détecté"

    # =========================
    # 5. FILTRE COMBINÉ : HORROR + BONNE NOTE
    # =========================
    horror_high_rated = df.filter(
        (pl.col("genre_names").str.contains("Horror", literal=False)) &
        (pl.col("vote_average") >= 7)
    )

    print("\n=== HORROR + HIGH RATING ===")
    print(f"Films Horror bien notés : {horror_high_rated.height}")

    assert horror_high_rated.height > 0, "Aucun film Horror bien noté"

    # =========================
    # 6. SAMPLE FINAL
    # =========================
    print("\n=== SAMPLE HORROR + HIGH RATING ===")

    sample = horror_high_rated.select(
        [
            "id",
            "title",
            "genre_names",
            "vote_average",
            "budget",
            "revenue",
        ]
    ).head(10)

    print(sample)

    # =========================
    # VALIDATION FINALE
    # =========================
    assert horror_df.height <= df.height
    assert high_rated_df.height <= df.height
    assert profitable_df.height <= df.height

    print("\n=== PIPELINE FILTERS OK ===")


if __name__ == "__main__":
    test_kaggle_pipeline_filters()