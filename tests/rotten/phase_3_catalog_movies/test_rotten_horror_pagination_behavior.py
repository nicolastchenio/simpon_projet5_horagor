from ingestion.rotten_client import RottenClient


def test_rotten_horror_pagination_behavior():
    """
    Test comportement pagination Rotten Tomatoes.

    Objectif :
    - vérifier que max_pages fonctionne correctement
    - vérifier que plus de pages = plus de résultats
    """

    client = RottenClient()

    try:
        # Page 1 uniquement
        page_1 = client.get_movie_links_paginated(
            base="movies_in_theaters",
            genre="horror",
            sort="a_z",
            selector='a[data-qa="discovery-media-list-item-caption"]',
            max_pages=1
        )

        # Page 2
        page_2 = client.get_movie_links_paginated(
            base="movies_in_theaters",
            genre="horror",
            sort="a_z",
            selector='a[data-qa="discovery-media-list-item-caption"]',
            max_pages=2
        )

        print("\n===== PAGINATION BEHAVIOR =====\n")
        print(f"Page 1: {len(page_1)} films")
        print(f"Page 2: {len(page_2)} films")

        # validation logique pagination
        assert len(page_1) > 0
        assert len(page_2) > 0

        # la page 2 doit contenir plus ou autant de résultats
        assert len(page_2) >= len(page_1)

        # validation format URLs
        assert all(
            m.startswith("https://www.rottentomatoes.com")
            for m in page_1 + page_2
        )

        assert all(
            "/m/" in m or "/tv/" in m
            for m in page_1 + page_2
        )

        print("\n[OK] Pagination site fonctionnelle")

    finally:
        client.close()


if __name__ == "__main__":
    test_rotten_horror_pagination_behavior()