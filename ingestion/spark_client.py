from pyspark.sql import SparkSession
from pathlib import Path


class SparkClient:
    """
    Client technique pour la manipulation de données avec PySpark.

    RESPONSABILITÉ :
    ----------------
    - Initialiser et gérer la SparkSession.
    - Charger des fichiers CSV bruts (ex: Kaggle).
    - Exporter les données dans des formats optimisés (ex: Parquet).
    - Fournir des outils d'inspection de DataFrame Spark.
    """

    def __init__(self, app_name: str = "HoragorIngestion"):
        """
        Initialise la session Spark.
        """
        self.spark = (
            SparkSession.builder
            .appName(app_name)
            .getOrCreate()
        )

    def stop(self):
        """
        Arrête la session Spark.
        """
        self.spark.stop()

    def load_csv(self, csv_path: str, header: bool = True, infer_schema: bool = True):
        """
        Charge un fichier CSV dans un DataFrame Spark.
        """
        path = Path(csv_path)
        if not path.exists():
            raise FileNotFoundError(f"Fichier CSV introuvable : {csv_path}")

        return (
            self.spark.read
            .format("csv")
            .option("header", str(header).lower())
            .option("inferSchema", str(infer_schema).lower())
            .load(str(path))
        )

    def save_to_parquet(self, df, output_path: str, mode: str = "overwrite"):
        """
        Enregistre un DataFrame au format Parquet.
        Utile pour optimiser les lectures futures.
        """
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        df.write.mode(mode).parquet(output_path)
        print(f"Données sauvegardées avec succès dans : {output_path}")

    def get_info(self, df):
        """
        Affiche les informations de base du DataFrame.
        """
        print("Schéma du DataFrame :")
        df.printSchema()
        
        row_count = df.count()
        col_count = len(df.columns)
        print(f"Dimensions : {row_count} lignes, {col_count} colonnes")
