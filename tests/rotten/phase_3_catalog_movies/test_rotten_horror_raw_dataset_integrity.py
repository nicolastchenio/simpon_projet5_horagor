from ingestion.rotten_client import RottenClient


def test_rotten_horror_raw_dataset_integrity():
    """
    Test intégrité du dataset brut Rotten Tomatoes.

    Objectifs :
    - vérifier que les données sont exploitables
    - vérifier unicité
    - vérifier format des URLs
    - vérifier stabilité minimale
    """

    client = RottenClient()

    try:
        movies = client.get_movie_links_paginated(
            base="movies_in_theaters",
            genre="horror",
            sort="a_z",
            selector='a[data-qa="discovery-media-list-item-caption"]',
            max_pages=2
        )

        print("\n===== RAW DATASET INTEGRITY =====\n")
        print(f"Total films: {len(movies)}")

        # 1. dataset non vide
        assert len(movies) > 0

        # 2. unicité (important pour dataset)
        assert len(movies) == len(set(movies)), "Doublons détectés"

        # 3. format URL valide (RT films + séries)
        for m in movies:
            assert m.startswith("https://www.rottentomatoes.com")
            assert "/m/" in m or "/tv/" in m

        # 4. stabilité minimale (dataset exploitable)
        assert len(movies) >= 5

        print("\nExtrait:")
        for m in movies[:5]:
            print(m)

        print("\n[OK] Dataset RAW cohérent")

    finally:
        client.close()


if __name__ == "__main__":
    test_rotten_horror_raw_dataset_integrity()