# processing/gold/run.py

import json
from pathlib import Path
from processing.gold.generator import GoldGenerator

# Chemins
INPUT_FILE = Path("data/fusioned/merged_dataset.json")
GOLD_DIR = Path("data/gold")
OUTPUT_FILE = GOLD_DIR / "gold_horror_movies.json"

def main():
    # 1. Chargement du dataset fusionné
    if not INPUT_FILE.exists():
        print(f"[ERROR] Merged dataset not found at {INPUT_FILE}. Please run Phase 6 first.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        merged_data = json.load(f)

    # 2. Initialisation du Générateur
    generator = GoldGenerator()

    # 3. Exécution de la génération Gold
    print(f"Generating Gold dataset from {len(merged_data)} merged movies...")
    gold_data = generator.process(merged_data)

    # 4. Sauvegarde
    GOLD_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(gold_data, f, indent=4, ensure_ascii=False)

    print(f"\n[OK] Gold dataset created: {OUTPUT_FILE}")
    print(f"Total Gold movies: {len(gold_data)} (Filtered from {len(merged_data)})")

if __name__ == "__main__":
    main()
