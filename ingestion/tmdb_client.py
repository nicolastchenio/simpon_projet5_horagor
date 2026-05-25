import requests
from app.config import TMDB_API_KEY


class TMDBClient:
    """
    Client permettant de communiquer avec l'API TMDB.
    uniquement des appels api (communuication avec api et methode de récupération des données)
    """

    # URL de base de l'API TMDB
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self):
        """
        Constructeur de la classe.
        Récupère la clé API depuis le fichier de configuration.
        """
        self.api_key = TMDB_API_KEY

    def _get(self, endpoint, params=None):
        """
        Méthode interne générique pour effectuer une requête GET.

        Args:
            endpoint (str):
                Endpoint de l'API TMDB
                Exemple : "/movie/popular"

            params (dict, optional):
                Paramètres supplémentaires de la requête
                Exemple : {"page": 1}

        Returns:
            dict:
                Réponse JSON convertie en dictionnaire Python

        Raises:
            Exception:
                Si la requête API échoue
        """

        # Si aucun paramètre n'est fourni,
        # on initialise un dictionnaire vide
        if params is None:
            params = {}

        # Ajout automatique de la clé API
        params["api_key"] = self.api_key

        # Construction de l'URL complète
        url = f"{self.BASE_URL}{endpoint}"

        # Envoi de la requête HTTP GET
        response = requests.get(url, params=params)

        # Vérification du code HTTP
        if response.status_code != 200:
            raise Exception(
                f"Erreur API TMDB: {response.status_code} - {response.text}"
            )

        # Conversion de la réponse JSON en dictionnaire Python
        return response.json()

    def get_popular_movies(self, page=1):
        """
        Récupère les films populaires depuis TMDB.

        Args:
            page (int):
                Numéro de page pour la pagination

        Returns:
            dict:
                Liste des films populaires
        """
        
        # Appel de la méthode interne pour effectuer la requête
        return self._get(
            "/movie/popular",
            {
                "page": page,
                "language": "fr-FR"
            }
        )
        
    def get_movie_genres(self):
        """
        Récupère la liste des genres de films disponibles sur TMDB.

        Returns:
            dict:
                Liste des genres de films
        """

        return self._get(
            "/genre/movie/list",
            {
                "language": "fr-FR"
            }
        )
    
    def get_horror_movies(self, page=1):
        """
        Récupère les films d'horreur depuis TMDB.

        Args:
            page (int):
                Numéro de page pour la pagination

        Returns:
            dict:
                Liste des films d'horreur
        """

        return self._get(
            "/discover/movie",
            {
                "language": "fr-FR",
                "sort_by": "popularity.desc",
                "with_genres": 27,
                "page": page
            }
        )
    
    def get_movie_details(self, movie_id):
        """
        Récupère les détails complets d'un film TMDB.

        Args:
            movie_id (int):
                Identifiant TMDB du film

        Returns:
            dict:
                Détails complets du film
        """

        return self._get(
            f"/movie/{movie_id}",
            {
                "language": "fr-FR"
            }
        )