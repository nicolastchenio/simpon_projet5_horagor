from ingestion.rotten_client import RottenClient


def test_movie_info():
    """
    Test extraction Movie Info Rotten Tomatoes.

    Objectif :
    - charger une page film
    - utiliser le client métier pour extraction
    - valider cohérence des données
    """

    client = RottenClient()

    try:
        # film stable de test
        url = "https://www.rottentomatoes.com/m/scream_2022"

        client.open_page(url)

        html = client.get_html()

        # extraction via client (logique métier centralisée)
        data = client.extract_movie_infos(html)

        print("\n===== MOVIE INFO EXTRACTED =====\n")

        for k, v in data.items():
            print(f"{k}: {v}")

        # -------------------------
        # assertions minimales pipeline
        # -------------------------

        assert data["synopsis"] is not None
        assert data["director"] is not None
        assert data["genre"] is not None

        print("\n[OK] Movie info extraction valide")

    finally:
        client.close()


if __name__ == "__main__":
    test_movie_info()