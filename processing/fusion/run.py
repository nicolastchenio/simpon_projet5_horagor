# processing/fusion/run.py

import json
from pathlib import Path
from processing.fusion.fuser import DataFuser

# Chemins
MATCHING_FILE = Path("data/matched/matching_table.json")
NORM_DIR = Path("data/normalized")
FUSIONED_DIR = Path("data/fusioned")
OUTPUT_FILE = FUSIONED_DIR / "merged_dataset.json"

def load_normalized_as_dict(source_name: str) -> dict:
    """Charge un dataset et le transforme en dict {id: movie}."""
    indexed_data = {}
    source_path = NORM_DIR / source_name
    if not source_path.exists():
        return {}
    
    for file in source_path.glob("normalized_*.json"):
        with open(file, "r", encoding="utf-8") as f:
            movies = json.load(f)
            for m in movies:
                indexed_data[m["id"]] = m
    return indexed_data

def main():
    # 1. Chargement de la table de matching
    if not MATCHING_FILE.exists():
        print("[ERROR] Matching table not found. Please run Phase 5 first.")
        return

    with open(MATCHING_FILE, "r", encoding="utf-8") as f:
        mapping_table = json.load(f)

    # 2. Chargement de tous les datasets normalisés
    print("Loading all normalized datasets into memory...")
    
    # Assurer que le dossier de sortie existe
    FUSIONED_DIR.mkdir(parents=True, exist_ok=True)
    
    datasets = {
        "tmdb": load_normalized_as_dict("tmdb"),
        "rotten": load_normalized_as_dict("rotten"),
        "kaggle": load_normalized_as_dict("kaggle"),
        "imdb": load_normalized_as_dict("imdb")
    }

    # 3. Initialisation du Fuser
    fuser = DataFuser(priority_order=["rotten", "kaggle", "imdb"])

    # 4. Exécution de la fusion
    print("Starting data fusion (MDM)...")
    merged_data = fuser.fuse_datasets(mapping_table, datasets)

    # 5. Sauvegarde
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, indent=4, ensure_ascii=False)

    print(f"\n[OK] Fusion complete: {OUTPUT_FILE}")
    print(f"Total merged movies: {len(merged_data)}")

if __name__ == "__main__":
    main()
