# processing/normalization/tmdb/run.py

import json
from pathlib import Path
from processing.normalization.tmdb.normalizer import TMDBNormalizer

CLEAN_DIR = Path("data/cleaned/tmdb")
NORM_DIR = Path("data/normalized/tmdb")
NORM_DIR.mkdir(parents=True, exist_ok=True)

normalizer = TMDBNormalizer()

for file in CLEAN_DIR.glob("cleaned_enriched_horror_page_*.json"):
    print(f"Normalizing TMDB: {file.name}")
    
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    normalized = normalizer.normalize_dataset(data)
    
    output_file = NORM_DIR / f"normalized_{file.name}"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(normalized, f, indent=4, ensure_ascii=False)
        
    print(f"[OK] TMDB normalized saved -> {output_file}")
