import polars as pl
from ingestion.kaggle_client import KaggleClient


def test_dataset_analysis():
    """
    Analyse détaillée du dataset Kaggle.

    Objectifs :
    ----------
    - lister toutes les colonnes
    - afficher leur type
    - mesurer leur complétude
    - mesurer leur cardinalité
    - afficher des exemples de valeurs

    Ce test est uniquement exploratoire.

    Il sert à préparer les futures décisions :
    - colonnes conservées
    - colonnes supprimées
    - colonnes utilisées pour le matching
    - colonnes utilisées pour l'enrichissement

    Aucune transformation métier n'est réalisée ici.
    """

    # =========================
    # CHARGEMENT DATASET
    # =========================
    client = KaggleClient(
        "data/raw/kaggle/horror_movies.csv"
    )

    df = client.load_dataset()

    print("\n===================================")
    print("       DATASET ANALYSIS")
    print("===================================\n")

    # =========================
    # OVERVIEW GLOBAL
    # =========================
    print("=== DATASET OVERVIEW ===")
    print(f"Lignes   : {df.height}")
    print(f"Colonnes : {df.width}")

    total_rows = df.height

    # =========================
    # ANALYSE DES COLONNES
    # =========================
    print("\n===================================")
    print("       COLUMN ANALYSIS")
    print("===================================")

    analysis_rows = []

    for column in df.columns:

        # ---------------------
        # TYPE DE DONNÉE
        # ---------------------
        dtype = str(df[column].dtype)

        # ---------------------
        # NOMBRE DE NULLS
        # ---------------------
        null_count = df[column].null_count()

        # ---------------------
        # TAUX DE REMPLISSAGE
        # ---------------------
        fill_rate = round(
            ((total_rows - null_count) / total_rows) * 100,
            2
        )

        # ---------------------
        # CARDINALITÉ
        # ---------------------
        unique_count = (
            df[column]
            .n_unique()
        )

        # ---------------------
        # EXEMPLES DE VALEURS
        # ---------------------
        examples = (
            df[column]
            .drop_nulls()
            .head(3)
            .to_list()
        )

        analysis_rows.append(
            {
                "column": column,
                "dtype": dtype,
                "nulls": null_count,
                "fill_rate_%": fill_rate,
                "unique_values": unique_count,
                "examples": str(examples)
            }
        )

    # =========================
    # AFFICHAGE DÉTAILLÉ
    # (plus lisible que le DataFrame)
    # =========================
    for row in analysis_rows:

        print("\n-----------------------------------")

        for key, value in row.items():
            print(f"{key:<15} : {value}")

    # =========================
    # DATAFRAME DE SYNTHÈSE
    # (utile pour filtrer)
    # =========================
    analysis_df = pl.DataFrame(
        analysis_rows
    )

    # =========================
    # COLONNES PEU REMPLIES
    # =========================
    print("\n===================================")
    print("     LOW FILL RATE COLUMNS")
    print("===================================")

    low_fill_columns = analysis_df.filter(
        pl.col("fill_rate_%") < 50
    )

    print(low_fill_columns)

    # =========================
    # FAIBLE CARDINALITÉ
    # =========================
    print("\n===================================")
    print("     LOW CARDINALITY COLUMNS")
    print("===================================")

    low_cardinality = analysis_df.filter(
        pl.col("unique_values") <= 10
    )

    print(low_cardinality)

    # =========================
    # ÉCHANTILLON COMPLET
    # =========================
    print("\n===================================")
    print("        SAMPLE DATASET")
    print("===================================")

    sample = df.head(5)

    for index, row in enumerate(
        sample.iter_rows(named=True),
        start=1
    ):

        print(f"\n========== ROW {index} ==========")

        for key, value in row.items():
            print(f"{key:<20}: {value}")

    # =========================
    # VALIDATION MINIMALE
    # =========================
    assert df.height > 0
    assert df.width > 0

    print("\n===================================")
    print("      ANALYSIS COMPLETED")
    print("===================================")


if __name__ == "__main__":
    test_dataset_analysis()