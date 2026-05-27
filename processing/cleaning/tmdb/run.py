# processing/cleaning/tmdb/run.py

import json
from pathlib import Path
from processing.cleaning.tmdb.cleaner import TMDBCleaner


# Dossier contenant les données brutes TMDB
RAW_DIR = Path("data/raw/tmdb")

# Dossier de sortie pour les données nettoyées
CLEAN_DIR = Path("data/cleaned/tmdb")

# Création du dossier si inexistant
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

# Initialisation du cleaner
cleaner = TMDBCleaner()


# Parcours de tous les fichiers enrichis TMDB
for file in RAW_DIR.glob("enriched_horror_page_*.json"):

    # Lecture du JSON brut
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Nettoyage du dataset complet
    cleaned = cleaner.clean_dataset(data)

    # Nom du fichier de sortie
    output_file = CLEAN_DIR / f"cleaned_{file.name}"

    # Sauvegarde du JSON nettoyé
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=4, ensure_ascii=False)

    # Log de suivi
    print(f"[OK] Cleaned dataset saved -> {output_file}")