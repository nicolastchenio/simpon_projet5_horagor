# processing/cleaning/kaggle/run.py

import json
from pathlib import Path
from processing.cleaning.kaggle.cleaner import (
    KaggleCleaner
)

# =====================================
# DOSSIERS
# =====================================

RAW_DIR = Path(
    "data/raw/kaggle"
)

CLEAN_DIR = Path(
    "data/cleaned/kaggle"
)

def main():
    # Création du dossier de sortie

    CLEAN_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # =====================================
    # INITIALISATION CLEANER
    # =====================================

    cleaner = KaggleCleaner()

    # =====================================
    # PARCOURS DATASETS
    # =====================================

    for file in RAW_DIR.glob(
        "horror_movies_selected.json"
    ):

        print(
            f"\nTraitement : {file.name}"
        )

        # -------------------------
        # Lecture dataset brut
        # -------------------------

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        # -------------------------
        # Nettoyage dataset
        # -------------------------

        cleaned = cleaner.clean_dataset(
            data
        )

        # -------------------------
        # Fichier de sortie
        # -------------------------

        output_file = (
            CLEAN_DIR
            / f"cleaned_{file.name}"
        )

        # -------------------------
        # Sauvegarde
        # -------------------------

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                cleaned,
                f,
                indent=4,
                ensure_ascii=False
            )

        # -------------------------
        # Logs
        # -------------------------

        print(
            f"[OK] Kaggle cleaned saved -> "
            f"{output_file}"
        )

        print(
            f"Films conservés : "
            f"{len(cleaned)}"
        )

if __name__ == "__main__":
    main()
