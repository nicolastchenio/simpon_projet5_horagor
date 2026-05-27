from ingestion.imdb_client import IMDbClient


def test_extract_movies():
    """
    Extraction brute d'un échantillon de films IMDb.

    Objectif :
    - visualiser les données réelles
    - analyser la qualité des champs
    """

    client = IMDbClient("data/raw/imdb/movie.sqlite")

    # récupération de 10 films
    movies = client.fetch_sample("movies", limit=10)

    print("\n=== EXTRACTION FILMS IMDb ===")

    for movie in movies:
        print(movie)
        print("-" * 80)

    client.close()


if __name__ == "__main__":
    test_extract_movies()