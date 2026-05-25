# Tmbd #
1) creation d'un compte tmbd => https://www.themoviedb.org/u/nico974
- https://www.themoviedb.org/?language=fr
- https://www.themoviedb.org/settings/api/request
- https://developer.themoviedb.org/docs/getting-started => tutoriel
2) creation d'une clé api => https://www.horagor.re

## Structurer des tests (important) ##

- Test 1 : connexion API  
   Commence par un endpoint basique qui ne nécessite pas de logique complexe => Endpoint : ` /movie/popular `
   vérifier :
   - que la clé API est valide
   - que tu reçois une réponse JSON exploitable
- Test 2 : récupération liste films  
   Analyser la structure JSON, observe les champs
   identifier ce que je vais garder et ce qui est inutile
- Test 3 : filtrage horror
   - Identifier l’ID du genre "horror" => Utilise l’endpoint : `/genre/movie/list `
   - Requête filtrée `/discover/movie ` avec filtre => genre = Horror
   Cela devient ta requête principale pour ton pipeline plus tard
- Test 4 : détails film  
   Endpoint détaillé `/movie/{movie_id} `  
   Objectif : voir toutes les données disponibles pour un film précis (overview, runtime, genres, production_companies, etc.)
- Test 5 : Tester les endpoints utiles pour enrichissement
  - ` /movie/{id}/credits ` → casting (IMDB-like)
  - ` /movie/{id}/reviews ` → critiques (utile pour RAG)
  - ` /movie/{id}/similar ` → recommandations
- Test 6 :Tester la pagination
   Les endpoints retournent des pages : vérifier combien de données on peut récupérer et estimer la volumétrie
- Test 7 :Tester les limites API
   combien de requêtes on peut faire, quel est le comportement en cas de limite

À la fin de cette phase, je dois avoir :
- Une bonne compréhension des endpoints
- Une liste claire des champs utiles
- Une stratégie de récupération des films d’horreur
- Une idée du volume de données

## Test api Tmbd ##
### test api ###

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

### Structuration du projet ###
```
project/
│
├── app/
│   ├── __init__.py
│   └── config.py
│
├── ingestion/
│   ├── __init__.py
│   └── tmdb_client.py
│
├── tests/
│   ├── __init__.py
│   │
│   └── tmdb/
│       ├── __init__.py
│       ├── test_popular_movies.py
│       └── test_movie_genres.py
│
├── .env
├── .gitignore
├── pyproject.toml
└── README.md
```
Creer :
- app/config.py => éviter de charger .env partout et centraliser la config
   ```
   import os
   from dotenv import load_dotenv

   load_dotenv()

   TMDB_API_KEY = os.getenv("TMDB_API_KEY")

   if not TMDB_API_KEY:
      raise ValueError("TMDB_API_KEY manquante dans .env")
   ```
- ingestion/tmdb_client.py => Créer le client TMDB
   ```
   import requests
   from app.config import TMDB_API_KEY


   class TMDBClient:
      BASE_URL = "https://api.themoviedb.org/3"

      def __init__(self):
         self.api_key = TMDB_API_KEY

      def _get(self, endpoint, params=None):
         if params is None:
               params = {}

         params["api_key"] = self.api_key

         url = f"{self.BASE_URL}{endpoint}"

         response = requests.get(url, params=params)

         if response.status_code != 200:
               raise Exception(f"Erreur API TMDB: {response.status_code} - {response.text}")

         return response.json()

      def get_popular_movies(self, page=1):
         return self._get("/movie/popular", {"page": page, "language": "fr-FR"})
   ```
- tests/test_tmdb.py => Adapter test_tmdb.
   ````
   from ingestion.tmdb_client import TMDBClient
   import json

   client = TMDBClient()

   data = client.get_popular_movies()

   print("Connexion API réussie\n")

   # Afficher le premier film complet
   first_movie = data["results"][0]

   print("-------- json du Premier film -----------\n")
   print(json.dumps(first_movie, indent=4, ensure_ascii=False))

   print("\n ---------------- Affichage des 5 premiers films populaires -------------\n")

   for movie in data.get("results", [])[:5]:
      print(f"id : {movie.get('id')}")
      print(f"Titre : {movie.get('title')}")
      print(f"Date : {movie.get('release_date')}")
      print(f"Note : {movie.get('vote_average')}")
      print("-" * 40)
   ````
- Tester 
=> depuis la racine du projet ``` uv run python -m tests.tmdb.test_popular_movies ```  
si je fais :
  - ` uv run python tests/tmdb/test_popular_movies.py `
  - ` uv run tests/tmdb/test_popular_movies.py `  
   j'ai une erreur `ModuleNotFoundError: No module named 'ingestion' ` catr python considére "tests/" comme point de départ mais n’inclut pas` automatiquement la racine du projet dans le  => ` from ingestion.tmdb_client import TMDBClient `ne trouve pas "ingestion"

- Autres fichiers tests creer :
  - ` uv run tests/tmdb/test_movie_genres.py `
  - ` uv run python -m tests.tmdb.test_horror_movies `
  - ` uv run python -m tests.tmdb.test_movie_details `
  - ` uv run python -m tests.tmdb.test_pagination `

---------------------------
### analyse des champs ###
1) Champs ESSENTIELS (à conserver)
Ce sont les champs centraux de ton projet.

      | Champ | Pourquoi |
      | :--- | :--- |
      | **id** | identifiant TMDB maître |
      | **imdb_id** | matching TMDB ↔ IMDB |
      | **title** | titre affiché |
      | **original_title** | utile matching international |
      | **overview** | très important pour le RAG |
      | **tagline** | enrichissement sémantique |
      | **genres** | filtrage et catégorisation |
      | **release_date** | matching + chronologie |
      | **runtime** | normalisation |
      | **vote_average** | score TMDB |
      | **popularity** | ranking/recommandation |

2) Champs IMPORTANTS pour enrichissement

   | Champ | Pourquoi |
   | :--- | :--- |
   | **budget** | enrichissement dataset |
   | **revenue** | enrichissement dataset |
   | **production_companies** | métadonnées intéressantes |
   | **production_countries** | analyses géographiques |
   | **original_language** | filtrage langues |
   | **spoken_languages** | enrichissement |
   | **status** | Released / Planned |

3) Champs UTILES pour le RAG
Très importants pour ton futur chatbot.

   | Champ | Utilité |
   | :--- | :--- |
   | **overview** | synopsis principal |
   | **tagline** | ambiance |
   | **genres** | contexte |
   | **title** | recherche |
   | **original_title** | recherche internationale |

> 👉 Ce sont probablement les champs les plus importants du futur RAG.

4) Champs importants pour le matching MDM
Tu en auras besoin lors de la fusion multi-sources.

   | Champ | Utilité |
   | :--- | :--- |
   | **id** | matching TMDB |
   | **imdb_id** | matching IMDB |
   | **title** | fallback matching |
   | **original_title** | matching fuzzy |
   | **release_date** | matching année |

## Début du pipline TMDB couche "RAW DATA LAYER" ##
1) Ajouter un dossier " data/raw/" au projet
- sauvegarder les données brutes TMDB
- conserver les réponses API
- préparer les traitements futurs

2) sauvegarder une page Horror en JSON brut
- data/raw/tmdb/ => exemple "data/raw/tmdb/horror_movies_page_1.json"

3) Créer un nouveau test "tests/tmdb/test_save_horror_movies.py":
- récupérer une page Horror
- sauvegarder le JSON brut  
plus tard cette logique migrera vers le vrai pipeline.

4) execution du fichier
` uv run python -m tests.tmdb.test_save_horror_movies `

Note :  
Pour l instant on recupere une liste de film d'horreur (avec get_horror_movies()) mais apres on fera de l enrichissement avec (get_horror_movies()).
Donc le pipline final réel:
```
DISCOVER (liste)
        ↓
ENRICH (détails)
        ↓
DATASET FINAL
```

## mini pipeline ingestion ##
- récupère plusieurs pages de films Horror
- sauvegarde chaque page en JSON
- prépare la base pour ingestion massive future

1) creer pipeline/tmdb_pipeline.py
- utiliser TMDBClient (ingestion)
- gérer pagination
- sauvegarder en data/raw/tmdb/
- rester réutilisable (pas un script “one-shot”)

   ```
   from ingestion.tmdb_client import TMDBClient
   from pathlib import Path
   import json
   import time


   class TMDBPipeline:
      """
      Pipeline d'ingestion TMDB pour les films Horror.
      Responsable de la récupération et du stockage des données brutes.
      """

      def __init__(self, output_dir="data/raw/tmdb"):
         self.client = TMDBClient()
         self.output_dir = Path(output_dir)
         self.output_dir.mkdir(parents=True, exist_ok=True)

      def fetch_page(self, page: int):
         """
         Récupère une page de films Horror depuis TMDB.
         """
         return self.client.get_horror_movies(page=page)

      def save_page(self, data: dict, page: int):
         """
         Sauvegarde une page de résultats en JSON.
         """
         file_path = self.output_dir / f"horror_movies_page_{page}.json"

         with open(file_path, "w", encoding="utf-8") as f:
               json.dump(data, f, indent=4, ensure_ascii=False)

         return file_path

      def run(self, max_pages: int = 3, sleep_time: float = 0.2):
         """
         Exécute le pipeline complet TMDB Horror.
         """
         print("=== Démarrage pipeline TMDB Horror ===\n")

         for page in range(1, max_pages + 1):

               print(f"Récupération page {page}...")

               data = self.fetch_page(page)
               file_path = self.save_page(data, page)

               print(f"Sauvegardé -> {file_path}")

               time.sleep(sleep_time)

         print("\n=== Pipeline terminé ===")
   ```

2) creer pipeline/main.py  
Il va orchestrer les pipeline (pour l'instant il n'y en a qu'un mais au final il y en aura plusieurs)

   ```
   from pipeline.tmdb_pipeline import TMDBPipeline


   def main():
      """
      Point d'entrée principal du projet.
      Lance les pipelines d'ingestion.
      """

      tmdb_pipeline = TMDBPipeline()

      # Test ingestion TMDB Horror
      tmdb_pipeline.run(max_pages=3)


   if __name__ == "__main__":
      main()
   ```
3) execution  
Depuis la racine : ` uv run python -m pipeline.main `
On obtient des fichier de type "horror_movies_page_1.json"

## enrichissement des données ##

- récupérer les détails de chaque film
- enrichir les données
- préparer un vrai dataset exploitable

Objectif pour obtenir :
- imdb_id
- runtime
- budget
- revenue
- overview complet
- tagline
- production_companies

1) Ajout de la méthode "enrich_movies()" dans TM tmdb_pipeline.py :
      ```
      def enrich_movies(self, movies: list):
        """
        Enrichit les films avec les détails complets TMDB.
        """

        enriched_movies = []

        for movie in movies:

            movie_id = movie.get("id")

            print(f"Enrichissement film TMDB ID : {movie_id}")

            # Récupération des détails complets
            details = self.client.get_movie_details(movie_id)

            enriched_movies.append(details)

            # Petite pause API
            time.sleep(0.2)

        return enriched_movies
      ```
2) Modifier la méthode run()
   ```
   def run(self, max_pages: int = 1):
      """
      Exécute le pipeline TMDB enrichi.
      """

      print("=== Démarrage pipeline TMDB Horror ===\n")

      for page in range(1, max_pages + 1):

            print(f"\nRécupération page {page}...")

            # Discover movies
            data = self.fetch_page(page)

            movies = data.get("results", [])

            print(f"{len(movies)} films récupérés")

            # Enrichissement détaillé
            enriched_movies = self.enrich_movies(movies)

            # Sauvegarde
            file_path = self.output_dir / f"enriched_horror_page_{page}.json"

            with open(file_path, "w", encoding="utf-8") as f:
               json.dump(
                  enriched_movies,
                  f,
                  indent=4,
                  ensure_ascii=False
               )

            print(f"Dataset enrichi sauvegardé -> {file_path}")

      print("\n=== Pipeline TMDB terminé ===")
   ```

3) execution  
Depuis la racine : ` uv run python -m pipeline.main `  
On obtient des fichier de type "enriched_horror_page_1.json"

## Transformation / nettoyage des données ##
Transformer les fichiers "data/raw/tmdb/enriched_horror_page_X.json" vers "data/cleaned/tmdb/cleaned_horror_page_X.json"

1) cleaning TMDB => processing/cleaning/tmdb_cleaning.py

   ```
   # processing/cleaning/tmdb_cleaning.py

   from typing import List, Dict, Any
   from datetime import datetime


   class TMDBCleaner:
      """
      Nettoyage strict TMDB selon schéma canonique projet.
      Objectif : garantir un dataset homogène pour RAG + matching + fusion.
      """

      def clean_movie(self, movie: Dict[str, Any]) -> Dict[str, Any]:

         # -----------------------------
         # 1. STRUCTURE CIBLE FIXE
         # -----------------------------
         cleaned = {
               # CORE DATA (MDM + RAG)
               "id": movie.get("id"),
               "imdb_id": movie.get("imdb_id"),
               "title": movie.get("title"),
               "original_title": movie.get("original_title"),
               "overview": movie.get("overview") or "",
               "tagline": movie.get("tagline") or "",

               # LISTES NORMALISÉES
               "genres": [],
               "release_date": movie.get("release_date"),
               "release_year": None,
               "runtime": movie.get("runtime"),
               "vote_average": movie.get("vote_average"),
               "popularity": movie.get("popularity"),

               # ENRICHISSEMENT
               "budget": movie.get("budget"),
               "revenue": movie.get("revenue"),
               "production_companies": [],
               "production_countries": [],
               "original_language": movie.get("original_language"),
               "spoken_languages": [],
               "status": movie.get("status"),
         }

         # -----------------------------
         # 2. GENRES
         # -----------------------------
         for g in movie.get("genres", []):
               if isinstance(g, dict) and g.get("name"):
                  cleaned["genres"].append(g["name"])

         # -----------------------------
         # 3. PRODUCTION COMPANIES
         # -----------------------------
         for c in movie.get("production_companies", []):
               if isinstance(c, dict) and c.get("name"):
                  cleaned["production_companies"].append(c["name"])

         # -----------------------------
         # 4. PRODUCTION COUNTRIES
         # -----------------------------
         for c in movie.get("production_countries", []):
               if isinstance(c, dict) and c.get("name"):
                  cleaned["production_countries"].append(c["name"])

         # -----------------------------
         # 5. SPOKEN LANGUAGES
         # -----------------------------
         for l in movie.get("spoken_languages", []):
               if isinstance(l, dict) and l.get("english_name"):
                  cleaned["spoken_languages"].append(l["english_name"])

         # -----------------------------
         # 6. RELEASE YEAR (MDM + FILTER)
         # -----------------------------
         try:
               if cleaned["release_date"]:
                  cleaned["release_year"] = datetime.strptime(
                     cleaned["release_date"], "%Y-%m-%d"
                  ).year
         except Exception:
               cleaned["release_year"] = None

         return cleaned

      def clean_dataset(self, movies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
         return [self.clean_movie(m) for m in movies]
   ```

2) script d’exécution => processing/cleaning/run_tmdb_cleaning.py
   ```
   import json
   from pathlib import Path
   from tmdb_cleaning import TMDBCleaner


   RAW_DIR = Path("data/raw/tmdb")
   CLEAN_DIR = Path("data/cleaned/tmdb")
   CLEAN_DIR.mkdir(parents=True, exist_ok=True)

   cleaner = TMDBCleaner()

   for file in RAW_DIR.glob("enriched_horror_page_*.json"):

      with open(file, "r", encoding="utf-8") as f:
         data = json.load(f)

      cleaned = cleaner.clean_dataset(data)

      output_file = CLEAN_DIR / f"cleaned_{file.name}"

      with open(output_file, "w", encoding="utf-8") as f:
         json.dump(cleaned, f, indent=4, ensure_ascii=False)

      print(f"Cleaned saved: {output_file}")
   ```

3) execution  
Depuis la racine : ` uv run python -m processing.cleaning.run_tmdb_cleaning `