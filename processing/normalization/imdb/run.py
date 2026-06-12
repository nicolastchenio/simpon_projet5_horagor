# processing/normalization/imdb/run.py

import json
from pathlib import Path
from processing.normalization.imdb.normalizer import IMDbNormalizer

CLEAN_DIR = Path("data/cleaned/imdb")
NORM_DIR = Path("data/normalized/imdb")

def main():
    NORM_DIR.mkdir(parents=True, exist_ok=True)

    normalizer = IMDbNormalizer()

    for file in CLEAN_DIR.glob("cleaned_imdb_movies.json"):
        print(f"Normalizing IMDb: {file.name}")
        
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        normalized = normalizer.normalize_dataset(data)
        
        output_file = NORM_DIR / f"normalized_{file.name}"
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(normalized, f, indent=4, ensure_ascii=False)
            
        print(f"[OK] IMDb normalized saved -> {output_file}")

if __name__ == "__main__":
    main()
