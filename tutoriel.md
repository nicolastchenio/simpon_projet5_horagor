# Tmbd #
1) creation d'un compte tmbd => https://www.themoviedb.org/u/nico974
2) creation d'une clé api => https://www.horagor.re

# Test api Tmbd #

1) Créer un fichier .env => ``` TMDB_API_KEY=ta_cle_api ```
2) Installer dépendances minimales => ``` uv add requests python-dotenv ```
3) Faire un premier test simple  
   Crée un fichier : ``` test_tmdb.py ```

   ```
   import os
   import requests
   from dotenv import load_dotenv

   # Charger les variables d'environnement
   load_dotenv()

   API_KEY = os.getenv("TMDB_API_KEY")

   if not API_KEY:
      raise ValueError("Clé API TMDB introuvable dans le fichier .env")

   # Endpoint TMDB
   url = "https://api.themoviedb.org/3/movie/popular"

   params = {
      "api_key": API_KEY,
      "language": "fr-FR",
      "page": 1
   }

   try:
      response = requests.get(url, params=params)

      # Vérification du statut HTTP
      if response.status_code != 200:
         print(f"Erreur API : {response.status_code}")
         print(response.text)
      else:
         data = response.json()

         print("Connexion API réussie\n")

         # Afficher quelques films
         for movie in data.get("results", [])[:5]:
               print(f"Titre : {movie.get('title')}")
               print(f"Date : {movie.get('release_date')}")
               print(f"Note : {movie.get('vote_average')}")
               print("-" * 40)

   except Exception as e:
      print(f"Erreur : {e}")
   ```
4) executer le script => ``` uv run python test_tmdb.py ```