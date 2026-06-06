# pipeline/kaggle.py

import json
from pathlib import Path

import polars as pl

from ingestion.kaggle_client import KaggleClient


class KagglePipeline:
    """
    Pipeline Kaggle.

    Responsabilités :
    -----------------
    - charger le dataset Kaggle brut
    - conserver uniquement les colonnes utiles
    - sauvegarder un dataset intermédiaire

    IMPORTANT :
    ------------

    Ce pipeline ne réalise AUCUN nettoyage.

    Les étapes suivantes seront réalisées
    dans les prochaines phases :

    - normalisation
    - nettoyage
    - gestion des valeurs manquantes
    - déduplication
    - mapping TMDB / IMDb / Rotten
    - fusion multi-sources
    - construction du Gold Dataset
    """

    # =========================
    # COLONNES CONSERVÉES
    # =========================
    #
    # Décision prise suite aux tests :
    #
    # - test_profile
    # - test_exploration_genres
    # - test_pipeline_filters
    # - test_dataset_analysis
    #
    # Colonnes supprimées :
    #
    # - "" (ancien index CSV)
    # - poster_path
    # - status
    # - adult
    # - backdrop_path
    # - collection
    # - collection_name
    #
    KEEP_COLUMNS = [

        # Identifiant film
        "id",

        # Titres
        "original_title",
        "title",

        # Langue originale
        "original_language",

        # Description
        "overview",
        "tagline",

        # Date de sortie
        "release_date",

        # Popularité
        "popularity",

        # Votes utilisateurs
        "vote_count",
        "vote_average",

        # Informations business
        "budget",
        "revenue",

        # Durée du film
        "runtime",

        # Genres
        "genre_names",
    ]

    def __init__(
        self,
        input_file="data/raw/kaggle/horror_movies.csv",
        output_dir="data/raw/kaggle"
    ):
        """
        Initialise le pipeline Kaggle.
        """

        # Client Kaggle
        self.client = KaggleClient(
            input_file
        )

        # Répertoire de sortie
        self.output_dir = Path(
            output_dir
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # =========================
    # CHARGEMENT DATASET
    # =========================
    def load_dataset(self):
        """
        Charge le dataset Kaggle brut.
        """

        return self.client.load_dataset()

    # =========================
    # SÉLECTION COLONNES
    # =========================
    def select_columns(
        self,
        df: pl.DataFrame
    ):
        """
        Conserve uniquement les colonnes utiles
        pour la suite du projet.

        Aucune transformation n'est réalisée.
        """

        return df.select(
            self.KEEP_COLUMNS
        )

    # =========================
    # RAPPORT PIPELINE
    # =========================
    def print_summary(
        self,
        raw_df: pl.DataFrame,
        selected_df: pl.DataFrame
    ):
        """
        Affiche un résumé du pipeline.
        """

        print("\n===================================")
        print("         KAGGLE PIPELINE")
        print("===================================")

        # ---------------------
        # Dataset brut
        # ---------------------
        print("\n=== RAW DATASET ===")

        print(
            f"Lignes   : {raw_df.height}"
        )

        print(
            f"Colonnes : {raw_df.width}"
        )

        # ---------------------
        # Dataset sélectionné
        # ---------------------
        print("\n=== SELECTED DATASET ===")

        print(
            f"Lignes   : {selected_df.height}"
        )

        print(
            f"Colonnes : {selected_df.width}"
        )

        # ---------------------
        # Colonnes supprimées
        # ---------------------
        removed_columns = sorted(
            set(raw_df.columns)
            - set(selected_df.columns)
        )

        print("\n=== REMOVED COLUMNS ===")

        for column in removed_columns:
            print(f"- {column}")

        # ---------------------
        # Colonnes conservées
        # ---------------------
        print("\n=== KEPT COLUMNS ===")

        for column in selected_df.columns:
            print(f"- {column}")

    # =========================
    # SAUVEGARDE DATASET
    # =========================
    def save_dataset(
        self,
        df: pl.DataFrame
    ):
        """
        Sauvegarde le dataset sélectionné.

        Format :
        --------
        JSON

        Pourquoi JSON ?

        - facile à lire
        - facile à déboguer
        - cohérent avec TMDB
        - cohérent avec Rotten
        - pratique avant les phases
          de nettoyage et mapping
        """

        output_file = (
            self.output_dir
            / "horror_movies_selected.json"
        )

        # Conversion DataFrame
        # -> liste de dictionnaires
        data = df.to_dicts()

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"\n[OK] Dataset sauvegardé : "
            f"{output_file}"
        )

        return output_file

    # =========================
    # PIPELINE COMPLET
    # =========================
    def run(self):
        """
        Exécute le pipeline complet.
        """

        print(
            "\n=== DÉMARRAGE PIPELINE KAGGLE ==="
        )

        # ---------------------
        # Chargement dataset brut
        # ---------------------
        raw_df = self.load_dataset()

        # ---------------------
        # Sélection colonnes
        # ---------------------
        selected_df = self.select_columns(
            raw_df
        )

        # ---------------------
        # Rapport
        # ---------------------
        self.print_summary(
            raw_df,
            selected_df
        )

        # ---------------------
        # Sauvegarde
        # ---------------------
        self.save_dataset(
            selected_df
        )

        print(
            "\n=== PIPELINE KAGGLE TERMINÉ ==="
        )