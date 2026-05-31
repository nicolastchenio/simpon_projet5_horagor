from ingestion.rotten_client import RottenClient


def test_rotten_movie_page():
    """
    Vérifie l'ouverture d'une page film Rotten Tomatoes.
    """

    client = RottenClient()

    try:
        # Film test stable (horror)
        movie_url = "https://www.rottentomatoes.com/m/scream_2022"

        client.open_page(movie_url)

        print("\n=== TEST PAGE FILM ROTTEN ===\n")

        # 1. titre HTML
        print("Titre page :")
        print(client.get_page_title())

        # 2. URL actuelle (anti-redirect check)
        print("\nURL actuelle :")
        print(client.driver.current_url)

        # 3. vérification simple de stabilité page
        assert "rottentomatoes" in client.driver.current_url

        print("\n[OK] Page film chargée correctement")

    finally:
        client.close()


if __name__ == "__main__":
    test_rotten_movie_page()