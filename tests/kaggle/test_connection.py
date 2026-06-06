from ingestion.kaggle_client import KaggleClient


def test_kaggle_connection():
    """
    Test de validation ingestion Kaggle.
    Objectif : vérifier que le dataset est lisible et exploitable.
    """

    client = KaggleClient("data/raw/kaggle/horror_movies.csv")

    df = client.load_dataset()

    assert df is not None, "Dataset non chargé"
    assert df.shape[0] > 0, "Dataset vide"
    assert len(df.columns) > 0, "Aucune colonne détectée"

    print("\n=== KAGGLE CONNECTION OK ===")
    print(f"Lignes : {df.shape[0]}")
    print(f"Colonnes : {df.shape[1]}")


if __name__ == "__main__":
    test_kaggle_connection()