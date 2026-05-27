from ingestion.imdb_client import IMDbClient


def test_imdb_connection():
    """
    Test simple :
    - ouverture base SQLite
    - récupération des tables
    """

    # chemin vers ta base IMDb
    client = IMDbClient("data/raw/imdb/movie.sqlite")

    tables = client.get_tables()

    print("\n=== TABLES IMDb ===")

    for table in tables:
        print("-", table[0])

    client.close()


if __name__ == "__main__":
    test_imdb_connection()