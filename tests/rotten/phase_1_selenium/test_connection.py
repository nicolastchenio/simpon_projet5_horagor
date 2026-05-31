from ingestion.rotten_client import RottenClient


def test_rotten_connection():
    """
    Vérifie la connexion Selenium vers Rotten Tomatoes.
    """

    client = RottenClient()

    try:
        client.open_homepage()
        
        print("\n=== TEST CONNEXION ROTTEN ===\n")

        print(client.get_page_title())

    finally:
        client.close()


if __name__ == "__main__":
    test_rotten_connection()