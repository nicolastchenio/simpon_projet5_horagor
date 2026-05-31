from ingestion.rotten_client import RottenClient


def test_one_base_movies():
    """
    Test scraping simple sur une seule base.
    """

    BASES = {
        "movies_tv_shows": "tv_series_browse"
        # "movies_in_theaters": "movies_in_theaters"
    }

    GENRE = "horror"
    SORT = "a_z"

    client = RottenClient()

    try:
        movies = client.get_movie_links_paginated(
            # base=BASES["movies_in_theaters"],
            base=BASES["movies_tv_shows"],
            genre=GENRE,
            sort=SORT,
            selector='a[data-qa="discovery-media-list-item-caption"]'
        )

        print("\n===== NUMBER OF MOVIES =====\n")
        print(f"Nombre résultats: {len(movies)}")

        assert len(movies) > 0

        assert all(
            "/m/" in m or "/tv/" in m
            for m in movies
        )

        assert all(
            m.startswith("https://www.rottentomatoes.com")
            for m in movies
        )

    finally:
        client.close()


if __name__ == "__main__":
    test_one_base_movies()