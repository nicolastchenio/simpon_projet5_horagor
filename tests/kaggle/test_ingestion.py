import polars as pl
from ingestion.kaggle_client import KaggleClient


def test_kaggle_ingestion():
    """
    Test ingestion Kaggle (Polars).

    Objectif :
    - vérifier chargement dataset
    - valider structure minimale
    - vérifier colonnes critiques
    - contrôler nulls essentiels
    - produire un aperçu exploitable pipeline
    """

    # =========================
    # INITIALISATION CLIENT
    # =========================
    client = KaggleClient("data/raw/kaggle/horror_movies.csv")

    # Chargement du dataset
    df = client.load_dataset()

    # =========================
    # CHECK GLOBAL DATASET
    # =========================
    assert df is not None, "Dataset non chargé"
    assert df.height > 0, "Dataset vide"
    assert df.width >= 15, "Dataset incomplet"

    print("\n=== INGESTION CHECK ===")
    print(f"Lignes : {df.height}")
    print(f"Colonnes : {df.width}")

    # =========================
    # CHECK COLONNES CRITIQUES
    # =========================
    required_columns = [
        "id",
        "title",
        "original_title",
        "release_date",
        "genre_names",
        "vote_average",
        "budget",
        "revenue",
        "runtime"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    assert len(missing) == 0, f"Colonnes manquantes : {missing}"

    print("\n=== COLONNES OK ===")
    print(required_columns)

    # =========================
    # CHECK NULLS CRITIQUES
    # =========================
    null_counts = df.select([
        pl.col("id").null_count().alias("id_nulls"),
        pl.col("title").null_count().alias("title_nulls"),
    ])

    id_nulls = null_counts["id_nulls"][0]
    title_nulls = null_counts["title_nulls"][0]

    assert id_nulls == 0, "ID contient des valeurs nulles"
    assert title_nulls == 0, "TITLE contient des valeurs nulles"

    print("\n=== NULL CHECK OK ===")
    print(null_counts)

    # =========================
    # SAMPLE DATA (POUR ANALYSE)
    # =========================
    print("\n=== SAMPLE ===")
    print(
        df.select([
            "id",
            "title",
            "genre_names",
            "vote_average"
        ]).head(5)
    )


if __name__ == "__main__":
    test_kaggle_ingestion()