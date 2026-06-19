# pipeline/spark.py

from pathlib import Path
from ingestion.spark_client import SparkClient


class SparkPipeline:
    """
    Pipeline PySpark.

    Responsabilités :
    -----------------
    - Initialiser le client Spark
    - Charger le fichier CSV brut Kaggle avec PySpark
    - Valider le chargement (vérifier que le DataFrame n'est pas vide et contient les colonnes attendues)
    - Sauvegarder le DataFrame au format Parquet pour optimiser les lectures futures
    - Fermer proprement la session Spark
    """

    CRITICAL_COLUMNS = ["id", "title", "release_date", "genre_names"]

    def __init__(
        self,
        input_file: str = "data/raw/kaggle/horror_movies.csv",
        output_dir: str = "data/raw/spark"
    ):
        """
        Initialise le pipeline Spark.
        """
        self.input_file = input_file
        self.output_dir = Path(output_dir)
        self.output_file = self.output_dir / "horror_movies.parquet"
        self.client = None

    def validate_dataframe(self, df) -> bool:
        """
        Valide le DataFrame Spark en vérifiant s'il n'est pas vide
        et s'il contient les colonnes critiques nécessaires.
        """
        # Vérifier que le DataFrame n'est pas vide
        row_count = df.count()
        if row_count == 0:
            print("[ERREUR] Le DataFrame est vide !")
            return False

        # Vérifier la présence des colonnes critiques
        columns = df.columns
        for col in self.CRITICAL_COLUMNS:
            if col not in columns:
                print(f"[ERREUR] La colonne critique '{col}' est absente du DataFrame !")
                return False

        print(f"[OK] Validation réussie : {row_count} lignes chargées et colonnes critiques validées.")
        return True

    def run(self):
        """
        Exécute le pipeline complet.
        """
        print("\n=== DÉMARRAGE DU PIPELINE SPARK ===")
        
        try:
            # 1. Initialiser le client Spark
            self.client = SparkClient(app_name="HoragorSparkPipeline")

            # 2. Charger le CSV brut
            print(f"Chargement du fichier CSV : {self.input_file}")
            df = self.client.load_csv(self.input_file)

            # 3. Afficher les informations de base
            self.client.get_info(df)

            # 4. Valider le DataFrame
            if not self.validate_dataframe(df):
                raise ValueError("La validation du DataFrame Spark a échoué.")

            # 5. Sauvegarder au format Parquet
            print(f"Sauvegarde au format Parquet vers : {self.output_file}")
            self.client.save_to_parquet(df, str(self.output_file))

            print("=== PIPELINE SPARK TERMINÉ AVEC SUCCÈS ===")

        except Exception as e:
            print(f"[ERREUR] Une erreur est survenue lors de l'exécution du pipeline Spark : {e}")
            raise e

        finally:
            # Toujours s'assurer d'arrêter proprement la session Spark
            if self.client:
                print("Arrêt de la session Spark...")
                self.client.stop()


if __name__ == "__main__":
    pipeline = SparkPipeline()
    pipeline.run()
