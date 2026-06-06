import polars as pl
from pathlib import Path


class KaggleClient:
    """
    Client technique pour les datasets Kaggle.

    RESPONSABILITÉ :
    ----------------
    - charger un dataset CSV
    - exposer les données brutes
    - fournir des outils génériques d'exploration

    PAS de logique métier.
    PAS de nettoyage.
    PAS de transformation.
    """

    def __init__(self, csv_path: str):

        self.csv_path = Path(csv_path)

        if not self.csv_path.exists():
            raise FileNotFoundError(
                f"Dataset introuvable : {self.csv_path}"
            )

        # Chargement unique du dataset
        self.df = pl.read_csv(self.csv_path)

    def load_dataset(self):
        """
        Retourne le dataset complet.
        """

        return self.df

    def get_shape(self):
        """
        Retourne :
        (nb_lignes, nb_colonnes)
        """

        return self.df.shape

    def get_columns(self):
        """
        Retourne la liste des colonnes.
        """

        return self.df.columns

    def get_sample(self, n: int = 10):
        """
        Retourne un échantillon du dataset.
        """

        return self.df.head(n)

    def get_dataset_info(self):
        """
        Informations générales du dataset.

        Retourne :
        - nombre de lignes
        - nombre de colonnes
        - estimation mémoire
        """

        return {
            "rows": self.df.height,
            "columns": self.df.width,
            "estimated_size_mb": round(
                self.df.estimated_size() / 1024**2,
                2
            )
        }

    def get_unique_values(self, column_name: str):
        """
        Retourne les valeurs distinctes d'une colonne.
        """

        self._validate_column(column_name)

        return (
            self.df
            .select(column_name)
            .unique()
            .drop_nulls()
            .to_series()
            .to_list()
        )

    def get_value_counts(self, column_name: str):
        """
        Retourne les fréquences des valeurs
        d'une colonne.
        """

        self._validate_column(column_name)

        return (
            self.df
            .group_by(column_name)
            .len()
            .sort("len", descending=True)
        )

    def get_column_dtype(self, column_name: str):
        """
        Retourne le type d'une colonne.
        """

        self._validate_column(column_name)

        return self.df.schema[column_name]

    def get_null_counts(self):
        """
        Nombre de valeurs nulles
        pour chaque colonne.
        """

        return self.df.null_count()

    def get_column_null_count(self, column_name: str):
        """
        Nombre de valeurs nulles
        pour une colonne.
        """

        self._validate_column(column_name)

        return (
            self.df
            .select(
                pl.col(column_name)
                .is_null()
                .sum()
            )
            .item()
        )

    def get_non_null_percentage(self, column_name: str):
        """
        Pourcentage de valeurs non nulles.
        """

        self._validate_column(column_name)

        total = self.df.height

        null_count = self.get_column_null_count(
            column_name
        )

        non_null = total - null_count

        return round(
            (non_null / total) * 100,
            2
        )

    def get_columns_summary(self):
        """
        Résumé rapide de toutes les colonnes.

        Retourne :
        - nom colonne
        - type
        - nombre de nulls
        - nombre de valeurs distinctes
        """

        summary = []

        for col in self.df.columns:

            summary.append(
                {
                    "column": col,
                    "dtype": str(
                        self.df.schema[col]
                    ),
                    "nulls": self.get_column_null_count(col),
                    "unique_values": (
                        self.df
                        .select(
                            pl.col(col).n_unique()
                        )
                        .item()
                    )
                }
            )

        return pl.DataFrame(summary)

    def filter_rows(
        self,
        column_name: str,
        value
    ):
        """
        Retourne toutes les lignes où une colonne
        possède exactement une valeur donnée.
        """

        self._validate_column(column_name)

        return self.df.filter(
            pl.col(column_name) == value
        )

    def search_in_column(
        self,
        column_name: str,
        value: str,
        case: bool = False
    ):
        """
        Recherche un texte dans une colonne.

        Exemple :
        - Horror dans genre_names
        - English dans original_language
        """

        self._validate_column(column_name)

        if case:
            pattern = value
        else:
            pattern = f"(?i){value}"

        return self.df.filter(
            pl.col(column_name)
            .cast(pl.Utf8)
            .fill_null("")
            .str.contains(pattern)
        )

    def _validate_column(
        self,
        column_name: str
    ):
        """
        Vérifie qu'une colonne existe.
        """

        if column_name not in self.df.columns:
            raise ValueError(
                f"Colonne inconnue : {column_name}"
            )