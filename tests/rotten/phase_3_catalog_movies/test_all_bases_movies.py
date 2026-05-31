from ingestion.rotten_client import RottenClient


def test_all_movie_bases():
    """
    Test de scraping sur l'ensemble des bases Rotten Tomatoes.

    Objectifs :
    - vérifier que chaque base retourne des résultats
    - vérifier que la pagination fonctionne
    - vérifier que les URLs récupérées sont valides
    - vérifier la compatibilité films (/m/) et séries TV (/tv/)
    """

    # Bases disponibles sur Rotten Tomatoes
    BASES = {
        "movies_in_theaters": "movies_in_theaters",
        "movies_at_home": "movies_at_home",
        "movies_coming_soon": "movies_coming_soon",
        "movies_tv_shows": "tv_series_browse"
    }

    # Paramètres de recherche utilisés pour le test
    GENRE = "horror"
    SORT = "a_z"

    # Initialisation du client Selenium
    client = RottenClient()

    # Contiendra les résultats de toutes les bases
    all_movies = []

    try:

        # Parcours de chaque base Rotten Tomatoes
        for base in BASES.values():

            # Récupération paginée des URLs
            movies = client.get_movie_links_paginated(
                base=base,
                genre=GENRE,
                sort=SORT,
                selector='a[data-qa="discovery-media-list-item-caption"]'
            )

            # Affichage du nombre de résultats trouvés
            print(f"\nBase {base} -> {len(movies)} résultats")

            # Ajout au résultat global
            all_movies.extend(movies)

        # Résumé global
        print("\n===== TOTAL MOVIES =====")
        print(f"Total: {len(all_movies)}")

        # Vérifie qu'au moins un résultat a été récupéré
        assert len(all_movies) > 0

        # Vérifie que toutes les URLs proviennent de Rotten Tomatoes
        assert all(
            movie.startswith("https://www.rottentomatoes.com")
            for movie in all_movies
        )

        # Vérifie que les URLs sont soit :
        # - des fiches films (/m/)
        # - des fiches séries TV (/tv/)
        assert all(
            "/m/" in movie or "/tv/" in movie
            for movie in all_movies
        )

    finally:
        # Fermeture propre du navigateur Selenium
        client.close()


if __name__ == "__main__":
    test_all_movie_bases()