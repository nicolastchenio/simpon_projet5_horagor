from ingestion.rotten_client import RottenClient


def test_one_base_movies_listing():
    """
    Test debug : scraping d'une seule base avec affichage des URLs.

    Objectifs :
    - vérifier une base unique
    - afficher les URLs récupérées
    - option max_pages
    """

    BASES = {
        "movies_tv_shows": "tv_series_browse",
        "movies_in_theaters": "movies_in_theaters",
    }

    GENRE = "horror"
    SORT = "a_z"

    # option debug : limite de pages (None = toutes les pages)
    # MAX_PAGES = None
    MAX_PAGES = 2

    client = RottenClient()

    try:
        movies = client.get_movie_links_paginated(
            base=BASES["movies_in_theaters"],
            # base=BASES["movies_tv_shows"],
            genre=GENRE,
            sort=SORT,
            selector='a[data-qa="discovery-media-list-item-caption"]',
            max_pages=MAX_PAGES
        )

        print("\n===== ONE BASE MOVIES (DEBUG) =====\n")
        print(f"Total films: {len(movies)}\n")

        # affichage limité à 10
        for m in movies[:10]:
            print(m)

        assert len(movies) > 0

        assert all(
            m.startswith("https://www.rottentomatoes.com")
            for m in movies
        )

        assert all(
            "/m/" in m or "/tv/" in m
            for m in movies
        )

    finally:
        client.close()


if __name__ == "__main__":
    test_one_base_movies_listing()