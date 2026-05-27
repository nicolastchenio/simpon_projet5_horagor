from ingestion.imdb_client import IMDbClient


def test_imdb_schema():
    """
    Analyse la structure complète des tables IMDb.

    Objectif :
    - comprendre les colonnes disponibles
    - préparer le mapping MDM (TMDB ↔ IMDb)
    """

    client = IMDbClient("data/raw/imdb/movie.sqlite")

    tables = client.get_tables()

    print("\n=== STRUCTURE BASE IMDb ===")

    # Parcours de toutes les tables
    for table in tables:
        table_name = table[0]

        print(f"\n--- TABLE : {table_name} ---")

        schema = client.get_table_schema(table_name)

        # schema = (cid, name, type, notnull, default_value, pk)
        for col in schema:
            col_name = col[1]
            col_type = col[2]
            is_pk = col[5]

            print(f"{col_name} | {col_type} | PK={is_pk}")

    client.close()


if __name__ == "__main__":
    test_imdb_schema()