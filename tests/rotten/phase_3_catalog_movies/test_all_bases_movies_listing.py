from ingestion.rotten_client import RottenClient


def test_all_movie_bases_listing():
    """
    Test debug multi-bases avec affichage des URLs.

    Objectifs :
    - scraper toutes les bases
    - afficher les URLs (comme catalogue brut)
    - tester robustesse globale
    """

    BASES = {
        "movies_in_theaters": "movies_in_theaters",
        "movies_at_home": "movies_at_home",
        "movies_coming_soon": "movies_coming_soon",
        "movies_tv_shows": "tv_series_browse"
    }

    GENRE = "horror"
    SORT = "a_z"

    # option debug : limite pages (None = toutes)
    MAX_PAGES = None
    # MAX_PAGES = 2

    client = RottenClient()

    all_movies = []

    try:
        for base in BASES.values():

            movies = client.get_movie_links_paginated(
                base=base,
                genre=GENRE,
                sort=SORT,
                selector='a[data-qa="discovery-media-list-item-caption"]',
                max_pages=MAX_PAGES
            )

            print(f"\n===== BASE {base} =====")
            print(f"{len(movies)} résultats")

            # afficher seulement quelques liens
            for m in movies[:10]:
                print(m)

            all_movies.extend(movies)

        print("\n===== GLOBAL DEBUG RESULT =====")
        print(f"Total: {len(all_movies)}")

        assert len(all_movies) > 0

        assert all(
            m.startswith("https://www.rottentomatoes.com")
            for m in all_movies
        )

        assert all(
            "/m/" in m or "/tv/" in m
            for m in all_movies
        )

    finally:
        client.close()


if __name__ == "__main__":
    test_all_movie_bases_listing()