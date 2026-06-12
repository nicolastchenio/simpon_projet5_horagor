# processing/normalization/kaggle/run.py

import json
from pathlib import Path
from processing.normalization.kaggle.normalizer import KaggleNormalizer

CLEAN_DIR = Path("data/cleaned/kaggle")
NORM_DIR = Path("data/normalized/kaggle")

def main():
    NORM_DIR.mkdir(parents=True, exist_ok=True)

    normalizer = KaggleNormalizer()

    for file in CLEAN_DIR.glob("cleaned_horror_movies_selected.json"):
        print(f"Normalizing Kaggle: {file.name}")
        
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        normalized = normalizer.normalize_dataset(data)
        
        output_file = NORM_DIR / f"normalized_{file.name}"
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(normalized, f, indent=4, ensure_ascii=False)
            
        print(f"[OK] Kaggle normalized saved -> {output_file}")

if __name__ == "__main__":
    main()
