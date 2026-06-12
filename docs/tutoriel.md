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

## Tests api Tmbd ##
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
  - ` uv run python -m tests.tmdb.test_movie_genres.py `
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

## Nettoyage des données / transformation ( pré-normalisation)  ##
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

# Base SQLite IMDB #

- site  => https://www.kaggle.com/code/priy998/imdb-sqlite
- fichier imdb-sqlite-DATASET => https://www.kaggle.com/datasets/priy998/imdbsqlitedataset

--------
- exploration schéma
- requêtes SQL
-  tables
- échantillonnage
- profiling local

## Phase 1 IMDb = "TESTS EXPLORATION" ##

1) Test 1 — connexion base SQLite

   Objectif :
   - vérifier ouverture DB
   - lister tables

   ``` SELECT name FROM sqlite_master WHERE type='table'; ```

2) Test 2 — analyse structure des tables

   Objectif :
   - comprendre schéma réel IMDb

   ```
   PRAGMA table_info(title_basics);
   PRAGMA table_info(title_ratings);
   ```

   PRAGMA est une commande spéciale SQLite utilisée pour :
   - inspecter la base de données
   - obtenir des métadonnées (structure, index, tables, etc.)
   - modifier certains comportements du moteur SQLite

   Ce n’est pas du SQL “standard”, mais spécifique à SQLite.

   Exemples utiles :
   - PRAGMA table_info(table_name) → structure d’une table
   - PRAGMA database_list → bases attachées
   - PRAGMA foreign_key_list(table_name) → clés étrangères

3) Test 3 — extraction brute films

   Objectif :voir contenu réel

   ``` SELECT * FROM title_basics LIMIT 20; ```

4) Test 4 — filtrage films (équivalent horror TMDB)

   Objectif : trouver films pertinents

   IMDb n’a pas “genre API”, mais souvent :

   ```
   SELECT * 
   FROM title_basics
   WHERE genres LIKE '%Horror%'
   LIMIT 20;
   ```
5) Test 5 — jointures essentielles

   Objectif : comprendre structure relationnelle

   Ex :
   ```
   SELECT *
   FROM title_basics b
   JOIN title_ratings r ON b.tconst = r.tconst
   LIMIT 20;
   ```

6) Test 6 — analyse qualité des données et identification des champs utiles (MDM)

Objectif :
- NULL values
- formats dates
- doublons
- titres incohérents

mapping TMDB ↔ IMDb
- tconst → imdb_id
- primaryTitle → title
- originalTitle → original_title
- startYear → release_year
- runtimeMinutes → runtime
- genres → genres

### tests sqlite de imdb ###
1) Teste de connexion a la Base de donnee imdb
- creer "ingestion/imdb_client.py"
- creer "tests/imdb/test_connection.py"
- executer ``` uv run python -m tests.imdb.test_connection ```
  
2) Test 2 (PRAGMA table_info) pour analyser la structure des tables IMDb.
- comprendre les colonnes de chaque table
- identifier types, clés primaires, champs exploitables pour le MDM

- creer "tests/imdb/test_schema.py"
- executer ``` uv run python -m tests.imdb.test_schema ```

   Note :  
   On voit qu'il n'y a apas de colonne "genres" donc on ne pourra pas trier ce dataset par genre "horror".  
   => On va utiliser TMDB comme source de vérité pour les genres 
    - TMDB = source principale des genres
    - IMDb = source enrichissement (rating, revenue, director)
   
   Matching via :
   - title
   - release_date
   - imdb_id (si dispo plus tard)

   Nouvelle logique propre (MDM) :
   ```
   TMDB (genre filtering) → base dataset
         ↓
   IMDb (enrichment join)
         ↓
   fusion
   ```

3) Test 3 — extraction brute films
- visualiser les vraies données
- comprendre le contenu réel du dataset
- identifier :
  - valeurs NULL
  - formats de dates
  - types réels
  - qualité des champs
  - colonnes utiles pour le MDM

- creer "tests/imdb/test_extract_movies.py"
- executer ``` uv run python -m tests.imdb.test_extract_movies ```

4) Test 4 — filtrage films (équivalent horror TMDB)

   =>  Ce n est pas possible car il n y a pas dans ce dataset de colonne "genre" ou categorie", ... qui permet de recuperer tout les film "horror"

5) Test 5 — jointures essentielles
- creer "tests/imdb/test_movies_directors.py"
- execuiter ``` uv run python -m tests.imdb.test_movies_directors ```

6) Test 6 — analyse qualité des données et identification des champs utiles (MDM) si il y en a
- creer "tests/imdb/test_data_quality.py"
- executer ``` uv run python -m tests.imdb.test_data_quality ```

## Pipeline IMDB ##

1) creer pipeline/imdb_pipeline.py
- connexion SQLite
- extraction films
- sauvegarde JSON brut dans data/raw/imdb/imdb_movies.json

Mais ici different de TMDB car :
- source = SQLite locale
- pas d’API

Donc le pipeline sera plus simple

enrichissement des données avec la table directors

uid => est intéressant  pour l'instant on ne l inetgre pas a notre enrichissement car il faut le valider par rapport au TMDB movie id avant exploitation

2) Mise à jour pipeline/main.py

3) execution  
Depuis la racine : `uv run python -m pipeline.main `. On obtient le fichier "imdb_movies.json"

##  Nettoyage des données / transformation ( pré-normalisation) ##
1) creer "processing/cleaning/imdb_cleaning.py"
2) creer "processing/cleaning/run_imdb_cleaning.py"

Harmonisation avec TMDB, même structure logique :
- genres list
- release_year
- overview/tagline standardisés

Objectif : structure propre par source
- mêmes noms de champs “généraux”
- mêmes types (list, string, int, etc.)
- valeurs nettoyées
- champs manquants acceptés

3) execution  
Depuis la racine : `uv run python -m processing.cleaning.run_imdb_cleaning `


# RESTRUCTURATION DU PROJET #

## processing\cleaning ##

```
processing/
│
├── cleaning/
│   ├── tmdb/
│   │   ├── cleaner.py
│   │   └── run.py
│   │
│   ├── imdb/
│   │   ├── cleaner.py
│   │   └── run.py
```

Actuellement IMDB:
- imdb_cleaning.py
- run_imdb_cleaning.py

Devient :
- processing/cleaning/imdb/cleaner.py
- processing/cleaning/imdb/run.py

Pour executer en fera ` uv run python -m processing.cleaning.imdb.run `

Actuellement TMDB :
- tmdb_cleaning.py
- run_tmdb_cleaning.py

Devient :
- processing/cleaning/tmdb/cleaner.py
- processing/cleaning/tmdb/run.py

Pour executer en fera ` uv run python -m processing.cleaning.tmdb.run `

## pipeline (renommage des fichiers) ##
Actuellement :

pipeline/  
- tmdb_pipeline.py  
- imdb_pipeline.py  
 - main.py  

Proposition simplifiée :
pipeline/  
- tmdb.py  
- imdb.py  
- runner.py

pour exercuter on fera maintenant depuis la racine : `uv run python -m pipeline.runner `

# Rotten tomatoes #

https://www.rottentomatoes.com/

installation de 
- selenium => ` uv add selenium `
- ChromeDriver => ` uv add webdriver-manager ` => avec selenium on en as pas besoin (car => ` driver = webdriver.Chrome() `)
- beautifulsoup => ` uv add beautifulsoup4 `

## Ingestion ##
```
ingestion/
    rotten_client.py
```

Responsabilité :
- Selenium
- ouverture pages
- extraction HTML
- parsing 
  

## Tests ##
```
tests/
└── rotten/
    ├── __init__.py
    │
    ├── phase_1_selenium/
    │   ├── __init__.py
    │   ├── test_connection.py
    │   └── test_movie_page.py
    │
    ├── phase_2_extraction/
    │   ├── __init__.py
    │   ├── test_movie_infos.py
    │   └── test_scores.py
    │
    ├── phase_3_catalog_movies/
    │   ├── __init__.py
    │   ├── test_one_base_movies.py
    │   ├── test_all_bases_movies.py   
    │   ├── test_one_base_movies_listing.py
    │   ├── test_all_bases_movies_listing.py   
    │   ├── test_rotten_horror_pagination_behavior.py
    │   └── test_rotten_horror_raw_dataset_integrity.py
    │
    ├── phase_4_robustness/
    │   ├── __init__.py
    │   ├── test_waits.py
    │   ├── test_error_handling.py
    │   └── test_antibot.py
    │
    └── phase_5_data_engineering/
        ├── __init__.py
        ├── test_matching.py
        └── test_data_quality.py
```
les tests doivent surtout couvrir :
- Selenium
- chargement dynamique
- parsing HTML
- robustesse scraping
- matching des films

1) Phase Selenium
- connexion Selenium
   - Vérifier :
     - Selenium fonctionne
     - ChromeDriver fonctionne
     - Rotten accessible
   - Vérifications
     - ouverture navigateur
     - chargement page
     - récupération du title

- ouverture page film  
accès direct à une fiche film
  - Vérifications
    - HTTP OK
    - page correctement chargée
    - pas de redirection anti-bot

2) Phase extraction film
   - scores
     - tomatometer
     - audience score
   - movie infos 
     - Core RAG
       - synopsis
       - genre
       - rating
     - Enrichissement MDM
       - director
       - producer
       - production_companies
       - distributor
     - Metadata dataset
       - runtime
       - box_office
       - release_date

3) Phase catalogue Horror
- récupération liste horror
- pagination / lazy loading => vérifier que le site supporte pagination / navigation pages
  - on essaye de verifier si :
    - page=1 ≠ page=2
    - e site répond bien à ?page=2
    - le scraper respecte la navigation
  - Parce que Rotten :
    - change souvent son DOM
    - peut ignorer ?page=
    - ou passer en lazy-loading JS sans pagination réelle
- integrité du datasets => vérifier qualité + cohérence dataset brut =>  
  - intégrité => pas de doublons
  - format =< URLs valides
  - cohérence +> structure homogène
  - stabilité scraping +> extraction répétable

4) Phase robustesse
- waits Selenium
  - Tester :
    - WebDriverWait
    - éléments async
    - timing JS

- gestion erreurs
   -Tester :
   - 404
   - films supprimés
   - pages incomplètes

- anti-bot
  - Observer :
    - limitations
    - captchas éventuels
    - ralentissements
  - Tester :
    - delays
    - user-agent
    - pauses

5) Phase data engineering
- matching TMDB ↔ Rotten
- qualité données

### les tests ###
- creer "tests/rotten/phase1_selenium/test_connection.py"
- executer => `uv run python -m tests.rotten.phase_1_selenium.test_connection `

- creer "tests/rotten/phase1_selenium/test_movie_page.py"
- executer => `uv run python -m tests.rotten.phase_1_selenium.test_movie_page `

- creer "tests/rotten/phase_2_extraction/test_movie_page.py"
- executer => `uv run python -m tests.rotten.phase_2_extraction.test_scores `

- creer "tests/rotten/phase_2_extraction/test_movie_infos.py"
- executer => `uv run python -m tests.rotten.phase_2_extraction.test_movie_infos `

- creer "tests/rotten/phase_3_catalog_movies/test_one_base_movies.py"
- executer => `uv run python -m tests.rotten.phase_3_catalog_movies.test_one_base_movies `

- creer "tests/rotten/phase_3_catalog_movies/test_all_bases_movies.py"
- executer => `uv run python -m tests.rotten.phase_3_catalog_movies.test_all_bases_movies `

- creer "tests/rotten/phase_3_catalog_movies/test_one_base_movies_listing.py"
- executer => `uv run python -m tests.rotten.phase_3_catalog_movies.test_one_base_movies_listing `

- creer "tests/rotten/phase_3_catalog_movies/test_all_bases_movies_listing.py"
- executer => `uv run python -m tests.rotten.phase_3_catalog_movies.test_all_bases_movies_listing `
- creer "tests/rotten/rotten/phase_3_catalog_movies/test_rotten_horror_pagination_behavior.py"
- executer => `uv run python -m tests.rotten.phase_3_catalog_movies.test_rotten_horror_pagination_behavior `

- creer "tests/rotten/rotten/phase_3_catalog_movies/test_rotten_horror_raw_dataset_integrity.py"
- executer => `uv run python -m tests.rotten.phase_3_catalog_movies.test_rotten_horror_raw_dataset_integrity `

## Pipeline ##
```
pipeline/
    rotten.py
```

Responsabilité :
- orchestration extraction
- sauvegarde raw JSON

```
from ingestion.rotten_client import RottenClient
from pathlib import Path
import json
import time


class RottenPipeline:
    """
    Pipeline RAW Rotten Tomatoes

    Équivalent TMDB phase 1 :
    - extraction paginée
    - stockage brut JSON
    - préparation future enrichissement
    """

    def __init__(self, output_dir="data/raw/rotten"):
        self.client = RottenClient()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # =========================
    # FETCH PAGE
    # =========================

    def fetch_page(self, base: str, page: int, genre="horror", sort="a_z"):
        """
        Récupère une page via pagination Selenium.
        """

        return self.client.get_movie_links_paginated(
            base=base,
            genre=genre,
            sort=sort,
            selector='a[data-qa="discovery-media-list-item-caption"]',
            max_pages=page  # important: contrôle pagination externe
        )

    # =========================
    # SAVE RAW PAGE
    # =========================

    def save_page(self, base_name: str, urls: list, page: int):
        """
        Sauvegarde une page brute en JSON.
        """

        file_path = self.output_dir / f"{base_name}_page_{page}.json"

        data = {
            "base": base_name,
            "page": page,
            "count": len(urls),
            "urls": urls
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return file_path

    # =========================
    # RUN PIPELINE
    # =========================

    def run(self, bases: dict, max_pages: int = 2, sleep_time: float = 0.5):
        """
        Pipeline RAW Rotten.

        - boucle sur bases
        - pagination contrôlée
        - sauvegarde page par page
        """

        print("\n=== DÉMARRAGE PIPELINE ROTTEN RAW ===\n")

        for base_name, base_value in bases.items():

            print(f"\n=== BASE {base_name} ===")

            for page in range(1, max_pages + 1):

                print(f"Récupération page {page}...")

                urls = self.client.get_movie_links_paginated(
                    base=base_value,
                    genre="horror",
                    sort="a_z",
                    selector='a[data-qa="discovery-media-list-item-caption"]',
                    max_pages=page
                )

                file_path = self.save_page(base_name, urls, page)

                print(f"Sauvegardé -> {file_path}")

                time.sleep(sleep_time)

        print("\n=== PIPELINE ROTTEN TERMINÉ ===")

    # =========================
    # CLEAN EXIT
    # =========================

    def close(self):
        self.client.close()
```
1) creation d'un test :
   ```
   tests/
   └── rotten/
      ├── __init__.py
      │
      ├── phase_test_pipeline/
      │   ├── __init__.py
      │   └── test_save_horror_movies.py
   ```

   - executer => `uv run python -m tests.rotten.phase_test_pipeline.test_save_horror_movies `

2) amelioration de rotten.py pour
- un pipeline orchestré propre (multi-pages)
- une couche standardisée RAW (structure stable future)
   ```  
   data/
      raw/
         rotten/
   ```
- une séparation claire :
  - DISCOVER (liste)
  - RAW STORAGE (page brute)
- utilisation de runner.py  
  => pour executer `uv run python -m pipeline.runner `

3) enrichissement des données  
Pour chaque URL : "https://www.rottentomatoes.com/m/1408" ouvrir la fiche film puis récupérer :
   - extract_movie_infos()
   - extract_movie_scores()  
  déjà codées dans RottenClient.

note : le test "test_save_horror_movies.py" n'est maintenant plus valide, le code ayant etait modifié. Il n a donc plus aucun interet et devrait être archiver


## Cleaning / transformation ( pré-normalisation) ##
```
processing/cleaning/rotten/
    cleaner.py
    run.py
```

Responsabilité :
- standardisation
- gestion NULL
- nettoyer les chaînes de caractères (strip)
- nettoyer les listes
- supprimer les doublons dans les listes
- uniformiser les None
- filtrer les films non Horror
- conserver la structure Rotten d'origine

Pas de renommage de colonnes.  
Pas de conversion de dates.  
Pas de conversion de runtime.  
Pas de normalisation métier.  

Résultat attendu :
```
data/
└── cleaned/
    └── rotten/
        cleaned_movies_at_home_enriched.json
        cleaned_movies_coming_soon_enriched.json
        cleaned_movies_in_theaters_enriched.json
        cleaned_tv_series_browse_enriched.json
```

Pour executer en fera `uv run python -m processing.cleaning.rotten.run `

# Kaggle horror-movies #

https://www.kaggle.com/datasets/evangower/horror-movies/data

## Ingestion ##
```
ingestion/
    kaggle_client.py
```

- charger le CSV
- vérifier qu'il existe
- retourner un DataFrame
- fournir quelques informations de base

faire 
- `uv add polars `
- `uv add pyarrow `
- `uv add numpy `

Car Polars s'appuie souvent sur Arrow pour les performances et cela te servira probablement plus tard pour :
- Parquet
- échanges entre DataFrames
- traitements analytiques
- dataset Gold

Polars utilise NumPy pour certaines conversions (to_numpy)

## tests ##
```
tests/kaggle/
 ├── test_connection.py
 ├── test_ingestion.py
 ├── test_profile.py
 ├── test_exploration_genres.py
 ├── test_pipeline_filters.py
 └── test_dataset_analysis.py

 ```

- test_ingestion.py
   vérifier que le dataset Kaggle est correctement chargé et exploitable pour le pipeline, au-delà de la simple connexion.

   On passe donc de “le fichier existe” à “les données sont structurées correctement pour ingestion pipeline” :
   Ce que ce test doit valider

   Sans multiplier les tests, tu veux couvrir 5 points clés :

      1. Colonnes attendues

         Ton dataset Kaggle :
         - id
         - title
         - original_title
         - overview
         etc.

         👉 Vérifie qu’elles existent.

      2. Types de base exploitables
      - id → numérique ou string convertible
      - release_date → texte date
      - genre_names → string
         
      3. Valeurs critiques non nulles
      Minimum pour ingestion :
      - id
      - title

      4. Cohérence globale
      - dataset non vide
      -nombre de lignes cohérent

      5. Aperçu rapide (debug pipeline)
      - sample exploitable

- test_profile.py
   Ce test doit répondre à 5 questions :
   1. Répartition des genres  
   Quels genres dominent ?
   2. Distribution des notes (vote_average)  
   Films bien notés / mal notés
   3. Complétude des données  
   taux de null global
   4. Analyse budget / revenue  
   films rentables vs non rentables
   5. Aperçu exploitable pipeline  
   sample structuré

- test_exploration_genres.py
   Passage d’un format brut → exploitable ML
   - Avant : "Horror, Thriller"
   - Après : ["Horror", "Thriller"]
   - Puis : exploded table (1 ligne = 1 genre)

- test_pipeline_filters.py
    - valider les filtres métier simples (genre, notes, revenus)
    - vérifier la cohérence des sous-ensembles
    - préparer la base pour exploitation analytique

- test_dataset_selection.py
  - identifier les colonnes conservées
  - identifier les colonnes supprimées
  - préparer le pipeline

### les testes ###
- creer "tests/kaggle/test_connection.py"
  - executer => `uv run python -m tests.kaggle.test_connection `
- creer "tests/kaggle/test_ingestion.py"
  - executer => `uv run python -m tests.kaggle.test_ingestion `
- creer "tests/kaggle/test_profile.py"
  - executer => `uv run python -m tests.kaggle.test_profile `
- creer "tests/kaggle/test_exploration_genres.py"
  - executer => `uv run python -m tests.kaggle.test_exploration_genres `
- creer "tests/kaggle/test_pipeline_filters.py"
  - executer => `uv run python -m tests.kaggle.test_pipeline_filters `
- creer "tests/kaggle/test_dataset_analysis.py"
  - executer => `uv run python -m tests.kaggle.test_dataset_analysis `

## Pipeline ##
```
pipeline/
    kaggle.py
```
Si votre prochaine phase est le nettoyage, alors le pipeline Kaggle ne doit faire qu'une seule chose :
- charger le CSV brut ;
- supprimer les colonnes définitivement inutiles ;
-sauvegarder le dataset quasi brut dans data/cleaned/kaggle.

Aucune transformation métier, aucune normalisation, aucun cast, aucun nettoyage.

Colonnes à conserver:

""
"id"
"original_title"
"title"
"original_language"
"overview"
"tagline"
"release_date"
"popularity"
"vote_count"
"vote_average"
"budget"
"revenue"
"runtime"
"genre_names"

Pour exercuter on fera maintenant depuis la racine : `uv run python -m pipeline.runner `

## Cleaning / transformation ( pré-normalisation) ##
```
processing/cleaning/kaggle/
    cleaner.py
    run.py
```
Responsabilité :
- nettoyer les chaînes de caractères
- convertir les valeurs vides en None
- extraire éventuellement release_year
- ne pas renommer les colonnes
- ne pas normaliser les genres
- ne pas modifier les types métier
- ne pas faire de mapping TMDB/IMDb/Rotten

# Normalization / Transformation (Schéma Pivot) #

L'objectif de cette phase est de transformer les datasets nettoyés de chaque source vers un **schéma pivot commun** afin de permettre le matching et la fusion.

## Travaux réalisés (Commun à toutes les sources) ##
1.  **Création d'un utilitaire de normalisation (`processing/normalization/utils.py`) :**
    *   `normalize_title` : Conversion en minuscules, suppression des accents et des caractères spéciaux pour le matching.
    *   `parse_iso_date` : Standardisation des dates au format ISO `YYYY-MM-DD`.
    *   `scale_score` : Mise à l'échelle de tous les scores sur une base de 0 à 10 (ex: 85% -> 8.5).
2.  **Schéma Pivot cible :**
    *   `id`, `imdb_id`, `title`, `matching_title`, `release_date`, `release_year`, `runtime`, `genres`, `overview`, `tagline`, `score`, `vote_count`, `budget`, `revenue`, `production_companies`, `original_language`, `source`.

### 1. TMDB Normalisation ###
*   **Source :** `data/cleaned/tmdb/`
*   **Actions :** 
    *   Extraction des noms de genres et de compagnies.
    *   Conservation de la **popularité** et du **poster_path**.
    *   Extraction simplifiée du **casting** (liste de noms).
*   **Script :** `uv run python -m processing.normalization.tmdb.run`

### 2. Rotten Tomatoes Normalisation ###
*   **Source :** `data/cleaned/rotten/`
*   **Actions :** 
    *   Conversion du runtime `"1h 41m"` en minutes.
    *   Parsing des dates.
    *   **Score :** Aligné sur `average_rating` (sur 10).
    *   Conservation des réalisateurs (**director**) et extraction du **casting**.
*   **Script :** `uv run python -m processing.normalization.rotten.run`

### 3. Kaggle Normalisation ###
*   **Source :** `data/cleaned/kaggle/`
*   **Actions :** Découpage de la chaîne de genres.
*   **Script :** `uv run python -m processing.normalization.kaggle.run`

### 4. IMDb Normalisation ###
*   **Source :** `data/cleaned/imdb/`
*   **Actions :** 
    *   Conservation de la **popularité** et du **réalisateur** (`director_name`).
    *   Alignement des scores.
*   **Script :** `uv run python -m processing.normalization.imdb.run`

---
Tous les fichiers normalisés sont générés dans le dossier `data/normalized/`.


# Matching #

L'objectif de cette phase est de réconcilier les films provenant des 4 sources différentes en identifiant ceux qui sont identiques, malgré des variations de titres.

### Travaux réalisés ###
1.  **Moteur de Matching (`processing/matching/matcher.py`) :**
    *   **Stratégie de réconciliation :** 
        *   Niveau 1 : Correspondance exacte sur `matching_title` + `release_year`.
        *   Niveau 2 : Fuzzy matching (similarité textuelle via `difflib.SequenceMatcher`) avec un seuil de **0.90** pour les films de la même année.

         Dans certains datasets (notamment TMDB), le champ release_year était à null car il n'était pas extrait de la release_date lors de la normalisation.  
         - Utilitaire : Ajout d'une fonction extract_year dans processing/normalization/utils.py pour extraire l'année de n'importe quel format de date.
         - Normaliseurs : Mise à jour des normaliseurs TMDB, Kaggle et IMDb pour garantir que release_year est systématiquement peuplé à partir de la release_date si le champ est manquant.  
  
         Les années sont maintenant correctement extraites des dates ISO (ex: 2026-05-13 -> 2026), ce qui améliore considérablement le taux de succès du matching.

2.  **Table de correspondance :**
    *   Génération d'un fichier central `data/matched/matching_table.json`.
    *   Ce fichier sert de "pont" entre les sources : il liste chaque film TMDB (source maîtresse) et associe les IDs correspondants dans Rotten Tomatoes, Kaggle et IMDb.
3.  **Script d'exécution :**
    *   `uv run python -m processing.matching.run`
    *   Le script affiche des statistiques de matching pour évaluer la qualité du recouvrement entre les sources.

### Structure du fichier `matching_table.json` : ###
```json
{
    "tmdb_id": 1339713,
    "title": "Obsession",
    "release_year": 2026,
    "matches": {
        "tmdb": 1339713,
        "rotten": "https://www.rottentomatoes.com/m/obsession_2026",
        "kaggle": 760161,
        "imdb": 43597
    }
}
```
 Son but est de servir de "pont" pour la phase suivante (la fusion).
   - Le matching est bien réalisé via le titre et l'année.
   - Le résultat stocké est l'ID de la source correspondante pour permettre au module de fusion de retrouver directement les données sans refaire tout le
     calcul de similarité.


# Fusion et Consolidation (MDM) #

L'objectif de cette phase est de créer un dataset unique et complet en fusionnant les informations des 4 sources selon une logique de priorité.

### Travaux réalisés ###
1.  **Module de Fusion (`processing/fusion/fuser.py`) :**
    *   **Logique de priorité :** TMDB (Source Maîtresse) > Rotten Tomatoes > Kaggle > IMDb.
    *   **Complétion intelligente :** Si un champ (synopsis, budget, durée, réalisateur, casting) est vide dans TMDB, le système va automatiquement chercher la valeur dans la source suivante selon l'ordre de priorité.
    *   **Agrégation des scores :** Conservation de tous les scores spécifiques (`score_rotten_critics`, `score_imdb`, etc.) pour permettre des analyses croisées.
    *   **Traçabilité :** Ajout d'une colonne `enrichment_sources` listant les sources ayant contribué à enrichir la fiche du film.
2.  **Dataset fusionné :**
    *   Génération du fichier `data/fusioned/merged_dataset.json`.
3.  **Script d'exécution :**
    *   `uv run python -m processing.fusion.run`

# Gold #

 c'est ici que l'on transforme une donnée "techniquement
  fusionnée" en un produit "prêt à l'emploi".

  Voici la stratégie détaillée de ce que nous allons faire :

  1. L'Objectif du Dataset "Gold"
  Le dataset fusionné actuel contient encore beaucoup de "bruit" technique et de colonnes intermédiaires. Le dataset Gold doit être :
   - Sélectif : On ne garde que les colonnes utiles pour l'utilisateur final et le moteur de recherche.
   - Parfaitement propre : Plus aucune valeur aberrante ou format incohérent.

  2. Structure du Dataset Gold (Colonnes retenues)
  On garde un schéma propre et efficace :
   - Identité : title, release_year, original_language.
   - Contenu : overview, tagline, genres, director, cast.
   - Qualité :
       - score_tmdb, score_imdb, score_rotten_critics, score_rotten_audience.
       - score_horragor : Une moyenne calculée des scores disponibles.
   - Métadonnées : runtime, budget, revenue, production_companies.

  3.On cré un nouveau module dans processing/gold/. Ce script va :
   -  Charger le merged_dataset.json.
   -  Appliquer une priorité de contenu : On élimine les films qui n'ont ni overview ni tagline (trop peu d'informations pour être intéressants)
   -  Calculer un Score Global : Faire une moyenne pondérée de tous les scores disponibles pour avoir une note unique "HorRAGor

   ```
   processing/
      └── gold/
         ├── generator.py  (Logique de transformation)
         └── run.py        (Script d'exécution)
   data/
   └── gold/
         └── gold_horror_movies.json
   ```
 
  **Script d'exécution :** ` uv run python -m processing.gold.run `

 Le résultat sera sauvegardé dans " data/gold/gold_horror_movies.json." Ce fichier sera la source de vérité pour l'importation dans la base de données Supabase (Phase 8-10).