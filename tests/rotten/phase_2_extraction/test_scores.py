from ingestion.rotten_client import RottenClient


def test_rotten_scores():
    """
    Test extraction scores Rotten Tomatoes.

    Objectif :
    - charger une page film
    - extraire les scores via client métier
    - valider cohérence des données
    """

    client = RottenClient()

    try:
        # film stable
        url = "https://www.rottentomatoes.com/m/scream_2022"

        client.open_page(url)

        html = client.get_html()

        # extraction via client métier
        scores = client.extract_movie_scores(html)

        print("\n===== SCORES EXTRAITS =====\n")

        for k, v in scores.items():
            print(f"{k}: {v}")

        # -------------------------
        # assertions minimales
        # -------------------------
        assert scores["tomatometer"] is not None
        assert scores["popcornmeter"] is not None

        print("\n[OK] Extraction scores valide")

    finally:
        client.close()


if __name__ == "__main__":
    test_rotten_scores()