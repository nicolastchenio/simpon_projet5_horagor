Objectif : construire un pipeline de données complet qui alimente une base fiable (“Gold dataset”) pour un futur système RAG.
Contraintes clés :
- Multi-sources (5 types différents)
- Fusion intelligente (MDM)
- Données propres, normalisées, dédupliquées
- Persistance structurée (ORM + base relationnelle)

# PLAN GLOBAL DU PROJET #
## Phase 1 — Cadrage et architecture ##

Définir les fondations avant toute implémentation.

### 1.1 Définir les entités principales ###

- Film (noyau central)
- Scores (TMDB, IMDB, Rotten Tomatoes)
- Métadonnées (dates, synopsis, popularité)
- Sources (traçabilité des données)

### 1.2 Définir les flux de données ###

Ingestion → Nettoyage → Normalisation → Matching → Fusion → Stockage

### 1.3 Choisir une architecture ###

- Pipeline modulaire (chaque source indépendante)
- Orchestrateur (script principal ou workflow type DAG)
- Stockage intermédiaire (raw / cleaned / gold)

## Phase 2 — Ingestion des données (collecte) ##

Objectif : récupérer les données de chaque source séparément.

### 2.1 API TMDB (source principale) ###

- https://www.themoviedb.org/?language=fr
- https://www.themoviedb.org/settings/api/request
- https://developer.themoviedb.org/docs/getting-started => tutoriel

- Extraire :
  - title
  - overview
  - release_date
  - vote_average
  - popularity
- Stocker brut

### 2.2 Web scraping Rotten Tomatoes (Selenium) ###

https://www.rottentomatoes.com/

- Extraire :
  - tomatometer_score
  - audience_score
  - critics_consensus
- Gérer :
  - pages dynamiques
  - délais / anti-bot

### 2.3 Fichiers Kaggle (Polars) ###

https://www.kaggle.com/datasets/evangower/horror-movies

- Charger CSV volumineux
- Sélectionner colonnes utiles
- Supprimer doublons (title + date)

### 2.4 Base SQLite IMDB ###

https://www.kaggle.com/code/priy998/imdb-sqlite

- Requête :
  - jointure title_basics + title_ratings
  - filtre genre = Horror
  - filtre qualité (numVotes ≥ 1000)

### 2.5 PySpark (Big Data) ###

- Traiter fichiers splittés
- Extraire infos textuelles (ex: synopsis, mots-clés)

## Phase 3 — Nettoyage des données ##

Objectif : rendre chaque source propre avant fusion.

### 3.1 Nettoyage général ###

- Suppression HTML
- Trim / espaces
- Encodage UTF-8

### 3.2 Gestion des doublons ###

- Par source
- Basé sur :
  - titre + date

### 3.3 Filtrage ###

Conserver uniquement :
- Horror / Gore

## Phase 4 — Normalisation ##

Objectif : homogénéiser les formats.

### 4.1 Dates ###

- Format unique : ISO 8601
- Cas particulier :
  - année seule → YYYY-01-01

### 4.2 Scores ###

- TMDB / IMDB → sur 10
- Rotten Tomatoes → conserver sur 100

### 4.3 Textes ###

- Nettoyage whitespace
- Uniformisation des champs (overview, synopsis)

## Phase 5 — Matching / Réconciliation (MDM) ##

Objectif : identifier les mêmes films entre sources.

### Niveaux de matching : ###

#### 5.1 Niveau 1 (prioritaire) ####

- tmdb_id

#### 5.2 Niveau 2 ####

- imdb_id

#### 5.3 Niveau 3 (fuzzy matching) ####

- titre + année
- algorithme :
  - distance de Levenshtein

## Phase 6 — Fusion des données ##

Objectif : créer une fiche film unique enrichie.

Stratégie de priorité :
1) TMDB (source maître)
2) Rotten Tomatoes
3) Kaggle
4) IMDB
5) Spark

Règles :
- Si donnée manquante → prendre source suivante
- Ne jamais écraser une donnée prioritaire par une source inférieure

## Phase 7 — Création du dataset “Gold” ##

Objectif : produire une base finale propre.

Caractéristiques :
- 1 film = 1 entrée
- Données complètes
- Pas de doublons
- Champs homogènes

## Phase 8 — Modélisation de la base de données ##

Méthodologie Merise :

### 8.1 MCD (Conceptuel) ###

- Entités :
  - Film
  - Score
  - Source
- Relations :
  - Film ↔ Scores
  - Film ↔ Source

8.2 MLD (Logique)

- Tables relationnelles
- Clés primaires / étrangères

### 8.3 MPD (Physique) ###

- Types SQL
- Index
- Contraintes

## Phase 9 — Implémentation ORM (SQLAlchemy) ##

Objectif : connecter code ↔ base.

- Définir classes (modèles)
- Mapper tables
- Gérer insertion / update

## Phase 10 — Déploiement Supabase ##

Objectif : rendre les données accessibles.

- Créer base PostgreSQL
- Déployer schéma
- Charger dataset Gold

## Phase 11 — Documentation technique ##

Obligatoire :

- Schéma MCD / MLD / MPD
- Diagramme pipeline
- Description des sources
- Stratégie de fusion
- Choix techniques

# STRUCTURE CONSEILLÉE DU PROJET #
```
project/
│
├── app/
│   ├── __init__.py
│   └── config.py
│
├── ingestion/  => récupèration des données”
│   ├── __init__.py
│   ├── tmdb_client.py
│   ├── rotten_client.py
│   ├── imdb_client.py
│   ├── kaggle_loader.py
│   └── spark_processor.py
│
├── processing/
│   │
│   ├── cleaning/ => suppression doublons, gestion des nulles, conversion de type, nettoyage textes, dates, colonnes inutiles, ...
│   │   ├── tmdb_cleaning.py
│   │   ├── imdb_cleaning.py
│   │   └── omdb_cleaning.py
│   │
│   ├── normalization/  => Responsable des données imbriquées JSON
│   │   ├── tmdb_normalization.py
│   │   ├── imdb_normalization.py
│   │   └── omdb_normalization.py
│   │
│   ├── matching/ => rapprochement TMDB / IMDb / OMDb, détection doublons entre sources, fuzzy matching
│   │   ├── tmdb_imdb_matching.py
│   │   └── entity_matching.py
│   │
│   ├── fusion/ => fusion TMDB + IMDb + Rotten Tomatoes
│   │   └── movie_fusion.py
│   │
│   └── utils/  => fonctions communes
│       ├── text_utils.py
│       └── dataframe_utils.py
│
├── database/
│   ├── models.py
│   └── session.py
│
├── pipeline/ => construction des datasets
│   └── main.py => orchestration
│   ├── tmdb_pipeline.py
│   ├── imdb_pipeline.py
│   └── rotten_pipeline.py
│
├── tests/
│   ├── tmdb/
│   ├── rotten/
│   ├── imdb/
│   ├── kaggle/
│   └── spark/
│
├── data/
│   ├── raw/ => données brutes non modifiées
│   │   ├── tmdb
│   ├── cleaned/ => données nettoyées
│   └── gold/ => données finales prêtes pour usage
│
├── docs/
│
├── .env
├── .gitignore
├── pyproject.toml
└── README.md
```

# LOGIQUE GLOBALE DU PIPELINE #
1) Collecter (multi-sources)
2) Nettoyer (par source)
3) Normaliser
4) Matcher
5) Fusionner
6) Produire dataset Gold
7) Stocker (Supabase)

# POINTS CRITIQUES À NE PAS NÉGLIGER #
- Gestion des IDs (clé du projet)
- Fuzzy matching bien calibré
- Qualité des données > quantité
- Respect strict du genre Horror
- Traçabilité des sources

Si nécessaire, l’étape suivante peut consister à détailler :
- le schéma de base de données (MCD/MLD)
- ou l’architecture technique du pipeline (plus avancée, type production)