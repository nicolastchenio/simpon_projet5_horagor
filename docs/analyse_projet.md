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

Le cleaner doit seulement faire
- nettoyage des chaînes (strip)
- gestion des None
- suppression des doublons
- nettoyage des listes
- filtrage Horror
- suppression d'éventuels caractères parasites


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
- Harmonisation des dates (ISO 8601).
- Standardisation des durées (minutes).
- Création de `matching_title` (lowercase, sans accents/spéciaux).
- Standardisation des listes : Transformer les genres et entreprises en listes de strings simples.
- Alignement des noms de colonnes pour la fusion.

## Phase 5 — Matching ##
- Jointure sur `matching_title` + `release_year`.
- Utilisation du Fuzzy Matching pour les titres (Levenshtein).
- Création d'une table de correspondance inter-sources.

## Phase 6 — Fusion des données ##
- Application de la priorité : TMDB > Rotten > Kaggle > IMDb.
- Complétion des champs manquants (synopsis, budget, etc.).
- Agrégation des différents scores de notation.
- Traçabilité : Ajouter une colonne sources_found pour savoir quelles sources ont contribué à ce film.


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

# STRUCTURE DU PROJET #
```
project/
│
├── app/
│   ├── __init__.py
│   └── config.py
│
├── ingestion/  => récupèration des données” (logique client metier)
│   ├── __init__.py
│   ├── tmdb_client.py
│   ├── rotten_client.py
│   ├── imdb_client.py
│   ├── kaggle_clienty.py
│   └── spark_client.py
│
├── processing/
│   │
│   ├── cleaning/ => suppression doublons, gestion des nulles, conversion de type, nettoyage textes, dates, colonnes inutiles, ...
│   │   ├── tmdb/
│   │   │   ├── cleaner.py
│   │   │   └── run.py
│   │   │
│   │   ├── imdb/
│   │   │   ├── cleaner.py
│   │   │   └── run.py
│   │   │
│   │   ├── omdb/
│   │   │   ├── cleaner.py
│   │   │   └── run.py
│   │   │
│   │   ├── kaggle/
│   │   │   ├── cleaner.py
│   │   │   └── run.py
│   │
│   ├── normalization/  
│   │   ├── tmdb/
│   │   │   ├── nomalizer.py
│   │   │   └── run.py
│   │   │
│   │   ├── imdb/
│   │   │   ├── nomalizer.py
│   │   │   └── run.py
│   │   │
│   │   ├── omdb/
│   │   │   ├── nomalizer.py
│   │   │   └── run.py
│   │   │
│   │   └── kaggle/
│   │       ├── nomalizer.py
│   │       └── run.py└── run.py
│   │
│   ├── matching/ 
│   │   ├── matcher.py
│   │   └── run.py
│   │
│   ├── fusion/
│   │   ├── fuser.py
│   │   └── run.py
│   │
│   └──gold/ 
│   │   ├── generator.py
│   │   └── run.py
│
├── pipeline/ => construction des datasets
│   ├── runner.py => orchestration
│   ├── tmdb.py
│   ├── imdb.py
│   ├── rotten.py
│   ├── kaggle.py
│   └── spark.py
│
├── database/
│   ├── __init__.py
│   ├── base.py => Contient la classe de base SQLAlchemy.
│   ├── session.py => Connexion PostgreSQL / Supabase.
│   ├── create_tables.py => Permet de créer la base.
│   ├── seed_gold.py
│   └── models/
│       ├── __init__.py => pour charger tous les modèles.
│       ├── associations.py => Tables N-N.
│       ├── film.py
│       ├── score.py
│       ├── acteur.py
│       ├── genre.py
│       ├── realisateur.py
│       └── societe_production.py
│
├── tests/
│   ├── tmdb/
│   ├── rotten/
│   ├── kaggle/
│   └── imdb/
│
├── data/
│   ├── raw/ => données brutes non modifiées
│   │   ├── tmdb/
│   │   ├── imdb/
│   │   ├── kaggle/
│   │   ├── spark/
│   │   │   └── horror_movies.parquet/
│   │   ├── rotten/
│   │   │   ├── movies_at_home
│   │   │   ├── movies_coming_soon
│   │   │   ├── movies_in_theaters
│   │   │   └── tv_series_browse
│   │   
│   ├── cleaned/ => données nettoyées
│   │   ├── tmdb/
│   │   ├── imdb/
│   │   ├── rotten/
│   │   └── kaggle/
│   │
│   ├── normalizes/ => données normalisées
│   │   ├── tmdb/
│   │   ├── imdb/
│   │   ├── rotten/
│   │   └── kaggle/
│   │
│   ├── matched/ => données matchées
│   │
│   ├── fusioned/ => données fusionnées
│   │
│   ├── gold/ => données finales prêtes pour usage
│   │   └── gold_horror_movies.json
│   │
│   └── database/ => données persistantes sqlite
│       └── horagor.db
│
├── docs/
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
