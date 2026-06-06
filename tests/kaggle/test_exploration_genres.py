import polars as pl
from ingestion.kaggle_client import KaggleClient


def test_exploration_genres():
    """
    Test d'exploration des genres du dataset Kaggle.

    Objectifs :
    - analyser la structure des genres
    - transformer genre_names en format exploitable
    - obtenir une distribution réelle des genres
    - vérifier la qualité des données
    """

    # =========================
    # CHARGEMENT DATASET
    # =========================
    client = KaggleClient("data/raw/kaggle/horror_movies.csv")
    df = client.load_dataset()

    print("\n===================================")
    print("     EXPLORATION GENRES")
    print("===================================\n")

    # =========================
    # 1. OVERVIEW DATASET
    # =========================
    print("=== DATASET OVERVIEW ===")
    print(f"Lignes : {df.height}")
    print(f"Colonnes : {df.width}")

    # =========================
    # 2. SÉLECTION DES COLONNES UTILES
    # =========================
    df_genres = df.select(
        [
            pl.col("id"),
            pl.col("title"),
            pl.col("genre_names"),
        ]
    ).drop_nulls()

    # =========================
    # 3. TRANSFORMATION DES GENRES
    # =========================
    # Conversion "Horror, Thriller" -> ["Horror", "Thriller"]
    df_genres = df_genres.with_columns(
        pl.col("genre_names")
        .str.split(",")
        .alias("genre_list")
    )

    # Nettoyage des espaces autour des genres
    df_genres = df_genres.with_columns(
        pl.col("genre_list")
        .list.eval(pl.element().str.strip_chars())
    )

    print("\n=== SAMPLE GENRES NETTOYÉS ===")
    print(df_genres.head(5))

    # =========================
    # 4. EXPLOSION DES GENRES
    # =========================
    # Une ligne = un genre
    df_exploded = df_genres.explode("genre_list")

    print("\n=== SAMPLE GENRES EXPLOSÉS ===")
    print(df_exploded.head(10))

    # =========================
    # 5. DISTRIBUTION DES GENRES
    # =========================
    genre_distribution = (
        df_exploded
        .group_by("genre_list")
        .len()
        .rename({"len": "count"})
        .sort("count", descending=True)
    )

    print("\n=== DISTRIBUTION DES GENRES ===")
    print(genre_distribution.head(15))

    # =========================
    # 6. FILMS HORROR UNIQUEMENT
    # =========================
    horror_movies = (
        df_exploded
        .filter(pl.col("genre_list") == "Horror")
        .select(["id", "title", "genre_list"])
        .head(10)
    )

    print("\n=== SAMPLE FILMS HORROR ===")
    print(horror_movies)

    # =========================
    # 7. STATISTIQUES PAR GENRE
    # =========================
    genre_stats = (
        df_exploded
        .group_by("genre_list")
        .agg(
            [
                pl.len().alias("count"),
                pl.col("id").n_unique().alias("unique_movies")
            ]
        )
        .sort("count", descending=True)
    )

    print("\n=== STATISTIQUES PAR GENRE ===")
    print(genre_stats.head(15))

    # =========================
    # 8. VÉRIFICATION QUALITÉ DATASET
    # =========================
    # Vérifie si certains films n'ont aucun genre après transformation
    missing_genres = (
        df_exploded
        .group_by("id")
        .len()
        .filter(pl.col("len") == 0)
    )

    print("\n=== CONTRÔLE QUALITÉ ===")
    print(f"Films sans genre détecté : {missing_genres.height}")

    print("\n=== TEST TERMINÉ ===")


if __name__ == "__main__":
    test_exploration_genres()