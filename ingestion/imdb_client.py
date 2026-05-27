import sqlite3
from pathlib import Path


class IMDbClient:
    """
    Client SQLite pour la base IMDb.

    Objectif actuel :
    - vérifier connexion à la base
    - lister les tables disponibles

    ⚠️ Pas encore de logique métier (cleaning / transformation)
    """

    def __init__(self, db_path: str):
        """
        Initialise la connexion à la base SQLite IMDb.
        """

        self.db_path = Path(db_path)

        # Vérifie que le fichier existe bien
        if not self.db_path.exists():
            raise FileNotFoundError(f"Base IMDb introuvable : {self.db_path}")

        # Connexion SQLite
        self.conn = sqlite3.connect(self.db_path)
        
        # Permet de récupérer les résultats sous forme de dictionnaires
        self.conn.row_factory = sqlite3.Row
        
        self.cursor = self.conn.cursor()

    def get_tables(self):
        """
        Retourne la liste des tables présentes dans la base SQLite.
        """

        query = """
        SELECT name
        FROM sqlite_master
        WHERE type='table';
        """

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_table_schema(self, table_name: str):
        """
        Retourne la structure d'une table SQLite via PRAGMA.

        Donne :
        - nom des colonnes
        - types
        - NULL / NOT NULL
        - clé primaire
        """

        query = f"PRAGMA table_info({table_name});"

        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetch_sample(self, table_name: str, limit: int = 20):
        """
        Extrait un échantillon brut d'une table.

        Utile pour :
        - exploration du dataset
        - contrôle qualité
        - compréhension des données réelles
        """

        query = f"SELECT * FROM {table_name} LIMIT {limit};"

        self.cursor.execute(query)

        rows = self.cursor.fetchall()

        # Conversion sqlite Row -> dict Python
        return [dict(row) for row in rows]
    
    def fetch_movies_with_directors(self, limit: int = 20):
        """
        Récupère des films avec leurs réalisateurs.

        Objectifs :
        - comprendre les relations entre tables
        - tester les jointures SQL
        - préparer les futurs traitements relationnels
        """

        query = """
        SELECT
            m.id,
            m.title,
            m.release_date,
            m.vote_average,
            d.name AS director_name,
            d.department
        FROM movies m
        JOIN directors d
            ON m.director_id = d.id
        LIMIT ?;
        """

        self.cursor.execute(query, (limit,))

        rows = self.cursor.fetchall()

        # Conversion vers dictionnaires Python
        return [dict(row) for row in rows]
    
    def analyze_null_values(self):
        """
        Analyse les valeurs NULL dans la table movies.

        Objectif :
        - identifier les colonnes incomplètes
        - préparer le cleaning
        """

        query = """
        SELECT
            COUNT(*) AS total_movies,

            SUM(CASE WHEN title IS NULL THEN 1 ELSE 0 END) AS null_title,

            SUM(CASE WHEN original_title IS NULL THEN 1 ELSE 0 END) AS null_original_title,

            SUM(CASE WHEN overview IS NULL THEN 1 ELSE 0 END) AS null_overview,

            SUM(CASE WHEN tagline IS NULL THEN 1 ELSE 0 END) AS null_tagline,

            SUM(CASE WHEN release_date IS NULL THEN 1 ELSE 0 END) AS null_release_date,

            SUM(CASE WHEN vote_average IS NULL THEN 1 ELSE 0 END) AS null_vote_average,

            SUM(CASE WHEN director_id IS NULL THEN 1 ELSE 0 END) AS null_director_id

        FROM movies;
        """

        self.cursor.execute(query)

        return dict(self.cursor.fetchone())
    
    def analyze_duplicates(self):
        """
        Recherche les doublons potentiels.

        Objectif :
        - préparer le matching
        - détecter incohérences dataset
        """

        query = """
        SELECT
            title,
            release_date,
            COUNT(*) AS duplicates_count
        FROM movies
        GROUP BY title, release_date
        HAVING COUNT(*) > 1
        ORDER BY duplicates_count DESC;
        """

        self.cursor.execute(query)

        rows = self.cursor.fetchall()

        return [dict(row) for row in rows]

    def analyze_invalid_dates(self):
        """
        Recherche les dates invalides ou manquantes.

        SQLite stocke ici les dates sous forme TEXT.
        """

        query = """
        SELECT
            id,
            title,
            release_date
        FROM movies
        WHERE release_date IS NULL
        OR release_date = ''
        OR length(release_date) != 10;
        """

        self.cursor.execute(query)

        rows = self.cursor.fetchall()

        return [dict(row) for row in rows]
    
    def analyze_title_differences(self, limit: int = 20):
        """
        Recherche les films où title != original_title.

        Utile pour :
        - internationalisation
        - fuzzy matching
        - qualité des données
        """

        query = """
        SELECT
            id,
            title,
            original_title
        FROM movies
        WHERE title != original_title
        LIMIT ?;
        """

        self.cursor.execute(query, (limit,))

        rows = self.cursor.fetchall()

        return [dict(row) for row in rows]
    
    def get_director_by_id(self, director_id):
        query = """
        SELECT name, gender, department
        FROM directors
        WHERE id = ?
        """
        self.cursor.execute(query, (director_id,))
        return self.cursor.fetchone()

    def close(self):
        """
        Ferme la connexion à la base.
        """
        self.conn.close()