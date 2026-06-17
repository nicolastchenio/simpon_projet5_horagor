# HorRAGor 🎬🩸

**HorRAGor** est un pipeline de données (ETL) complet conçu pour construire une base de connaissance "Gold" ultra-fiable sur les films d'horreur. Ce dataset final est destiné à alimenter un futur système de **RAG (Retrieval-Augmented Generation)** pour un chatbot spécialisé dans le cinéma de genre.

---

## 🚀 Objectifs du Projet

- **Multi-sources** : Ingestion de données depuis 4 sources majeures (TMDB, IMDb, Rotten Tomatoes, Kaggle).
- **Master Data Management (MDM)** : Fusion intelligente des données avec gestion de priorités.
- **Qualité de donnée** : Nettoyage strict, normalisation et déduplication via fuzzy matching.
- **Persistance Cloud** : Stockage final sur **Supabase (PostgreSQL)** pour une accessibilité totale.

---

## 🏗️ Architecture & Structure du Projet

```text
.
├── app/                # Configuration globale
├── data/               # Stockage des données (Raw -> Cleaned -> Normalized -> Gold)
├── database/           # Modèles SQLAlchemy et scripts de migration
├── docs/               # Documentation technique et analyses
├── ingestion/          # Clients métiers (API TMDB, Selenium Rotten, etc.)
├── pipeline/           # Orchestration de l'ingestion brute
├── processing/         # Nettoyage, Normalisation, Matching, Fusion et Gold
├── tests/              # Scripts d'analyse et d'exploration des jeux de données
├── main.py             # Orchestrateur global du processus
└── pyproject.toml      # Gestion des dépendances
```

---

## 🗄️ Évolution de la Base de Données

Le projet a suivi une montée en charge progressive pour la gestion de la persistance :

1.  **SQLite** : Utilisation initiale pour l'exploration des données IMDb et les premiers tests locaux de stockage.
2.  **PostgreSQL (Local)** : Migration vers un environnement relationnel robuste pour gérer les relations complexes (N-N) entre films, acteurs, et genres.
3.  **Supabase** : Déploiement final sur le cloud pour rendre les données accessibles à distance et préparer l'intégration du futur chatbot RAG.

---

## ⚙️ Cycle de Traitement & Commandes

Le pipeline peut être lancé intégralement via l'orchestrateur ou étape par étape.

### 1. Orchestration Globale
Pour lancer tout le processus (Ingestion + Processing + Gold) :
```bash
# Exécution sur un échantillon (ex: 10 pages)
uv run python main.py 10

# Exécution complète
uv run python main.py
```

### 2. Ingestion & Processing
```bash
# Ingestion brute
uv run python -m pipeline.runner

# Processing complet (étapes individuelles disponibles dans processing/)
uv run python -m processing.matching.run
uv run python -m processing.fusion.run
uv run python -m processing.gold.run
```

### 3. Persistance (Supabase / PostgreSQL)
```bash
# Création des tables sur Supabase (via SQLAlchemy)
uv run python -m database.create_tables

# Injection du dataset Gold dans le Cloud
uv run python -m database.seed_gold
```

---

## 📊 Exploration & Analyse des Données

Le dossier `tests/` contient des scripts dédiés à la validation de la qualité des données par source :
```bash
uv run python -m tests.kaggle.test_profile
uv run python -m tests.rotten.phase_1_selenium.test_connection
```

---

## 🛠️ Configuration & Déploiement

### Pré-requis
- Python 3.12+
- [uv](https://github.com/astral-sh/uv)
- Compte **Supabase** (gratuit)

### Installation
1. Clonez le dépôt et installez les dépendances : `uv sync`.
2. Configurez votre `.env` en utilisant l'URL de connexion fournie par Supabase :
   ```env
   TMDB_API_KEY=votre_cle_api
   DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres
   ```
3. Si vous utilisez Supabase pour la première fois, assurez-vous d'accorder les droits sur le schéma public :
   ```sql
   GRANT ALL ON SCHEMA public TO postgres;
   ALTER SCHEMA public OWNER TO postgres;
   ```

---

## 🛠️ Stack Technique

- **Langage** : Python 3.12
- **Data** : SQLite (IMDb Raw), JSON/CSV
- **Scraping** : Selenium, BeautifulSoup4
- **Base de données** : PostgreSQL (Local) & **Supabase (Cloud)**
- **ORM** : SQLAlchemy
- **Gestionnaire** : `uv`
