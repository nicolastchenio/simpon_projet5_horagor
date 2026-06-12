import json
from pathlib import Path
from processing.matching.matcher import MovieMatcher

# Chemins des données normalisées
NORM_DIR = Path("data/normalized")
MATCHED_DIR = Path("data/matched")
OUTPUT_FILE = MATCHED_DIR / "matching_table.json"

def load_normalized_data(source_name: str) -> list:
    data = []
    source_path = NORM_DIR / source_name
    if not source_path.exists():
        return []
    
    for file in source_path.glob("normalized_*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data.extend(json.load(f))
    return data

def main():
    matcher = MovieMatcher(threshold=0.90) # Seuil strict pour éviter les faux positifs

    # Chargement des datasets
    print("Loading normalized datasets...")
    
    # Assurer que le dossier de sortie existe
    MATCHED_DIR.mkdir(parents=True, exist_ok=True)
    
    tmdb_data = load_normalized_data("tmdb")
    rotten_data = load_normalized_data("rotten")
    kaggle_data = load_normalized_data("kaggle")
    imdb_data = load_normalized_data("imdb")

    if not tmdb_data:
        print("[ERROR] No TMDB data found. Matching impossible.")
        return

    sources = {
        "rotten": rotten_data,
        "kaggle": kaggle_data,
        "imdb": imdb_data
    }

    # Création du mapping
    mapping_table = matcher.create_mapping(tmdb_data, sources)

    # Sauvegarde
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping_table, f, indent=4, ensure_ascii=False)

    print(f"\n[OK] Matching table created: {OUTPUT_FILE}")
    print(f"Total master movies: {len(mapping_table)}")
    
    # Statistiques rapides
    stats = {"rotten": 0, "kaggle": 0, "imdb": 0}
    for entry in mapping_table:
        for src in stats.keys():
            if entry["matches"][src]:
                stats[src] += 1
    
    print("\nMatching Stats:")
    for src, count in stats.items():
        percent = (count / len(mapping_table)) * 100
        print(f"- {src.upper()}: {count} matches ({percent:.1f}%)")

if __name__ == "__main__":
    main()
