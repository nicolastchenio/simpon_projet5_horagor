# processing/cleaning/rotten/run.py

import json
from pathlib import Path
from processing.cleaning.rotten.cleaner import RottenCleaner


# ==================================================
# DOSSIERS
# ==================================================

# Dossier contenant les datasets enrichis Rotten
RAW_DIR = Path("data/raw/rotten")

# Dossier de sortie des datasets nettoyés
CLEAN_DIR = Path("data/cleaned/rotten")

# Création du dossier si nécessaire
CLEAN_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==================================================
# INITIALISATION DU CLEANER
# ==================================================

cleaner = RottenCleaner()


# ==================================================
# PARCOURS DES DATASETS ENRICHIS
# ==================================================

for file in RAW_DIR.glob("*_enriched.json"):

    print(f"\nTraitement : {file.name}")

    # ----------------------------------------------
    # Lecture du dataset brut enrichi
    # ----------------------------------------------

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    # ----------------------------------------------
    # Nettoyage complet du dataset
    # ----------------------------------------------

    cleaned = cleaner.clean_dataset(data)

    # ----------------------------------------------
    # Construction du nom du fichier de sortie
    # ----------------------------------------------

    output_file = (
        CLEAN_DIR /
        f"cleaned_{file.name}"
    )

    # ----------------------------------------------
    # Sauvegarde du dataset nettoyé
    # ----------------------------------------------

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

    # ----------------------------------------------
    # Logs de suivi
    # ----------------------------------------------

    print(
        f"[OK] Rotten cleaned saved -> {output_file}"
    )

    print(
        f"Films conservés : {len(cleaned)}"
    )