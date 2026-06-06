import polars as pl
from ingestion.kaggle_client import KaggleClient


def test_kaggle_profile():
    """
    Test de profiling du dataset Kaggle (Polars).

    Objectif :
    - comprendre la distribution globale
    - identifier les patterns métier
    - préparer le nettoyage et le matching
    """

    # =========================
    # CHARGEMENT DATASET
    # =========================
    client = KaggleClient("data/raw/kaggle/horror_movies.csv")
    df = client.load_dataset()

    print("\n==============================")
    print("       KAGGLE PROFILE")
    print("==============================\n")

    # =========================
    # 1. OVERVIEW DATASET
    # =========================
    print("=== DATASET OVERVIEW ===")
    print(f"Lignes : {df.height}")
    print(f"Colonnes : {df.width}")

    # =========================
    # 2. NULL RATE GLOBAL
    # =========================
    null_rate = (
        df
        .select(pl.all().is_null())
        .to_numpy()
        .mean()
    )

    null_summary = pl.DataFrame({
        "null_rate_global": [null_rate]
    })

    print("\n=== NULL RATE GLOBAL ===")
    print(null_summary)

    # =========================
    # 3. DISTRIBUTION GENRES
    # =========================
    print("\n=== GENRE DISTRIBUTION (RAW) ===")

    genre_counts = (
        df
        .select(pl.col("genre_names"))
        .drop_nulls()
        .group_by("genre_names")
        .len()
        .rename({"len": "count"})
        .sort("count", descending=True)
        .head(10)
    )

    print(genre_counts)

    # =========================
    # 4. STATISTIQUES VOTE AVERAGE
    # =========================
    print("\n=== VOTE AVERAGE STATS ===")

    vote_stats = df.select(
        [
            pl.col("vote_average").mean().alias("mean_vote"),
            pl.col("vote_average").min().alias("min_vote"),
            pl.col("vote_average").max().alias("max_vote"),
            pl.col("vote_average").median().alias("median_vote"),
        ]
    )

    print(vote_stats)

    # =========================
    # 5. PROFITABILITÉ
    # =========================
    print("\n=== PROFITABILITY ANALYSIS ===")

    profit_analysis = df.select(
        [
            (pl.col("revenue") - pl.col("budget")).mean().alias("avg_profit"),
            (pl.col("revenue") > pl.col("budget")).mean().alias("profit_ratio"),
        ]
    )

    print(profit_analysis)

    # =========================
    # 6. SAMPLE DATA
    # =========================
    print("\n=== SAMPLE DATA ===")

    sample = df.select(
        [
            "id",
            "title",
            "genre_names",
            "vote_average",
            "budget",
            "revenue",
        ]
    ).head(5)

    print(sample)


if __name__ == "__main__":
    test_kaggle_profile()