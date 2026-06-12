# processing/normalization/rotten/run.py

import json
from pathlib import Path
from processing.normalization.rotten.normalizer import RottenNormalizer

CLEAN_DIR = Path("data/cleaned/rotten")
NORM_DIR = Path("data/normalized/rotten")
NORM_DIR.mkdir(parents=True, exist_ok=True)

normalizer = RottenNormalizer()

for file in CLEAN_DIR.glob("cleaned_*_enriched.json"):
    print(f"Normalizing Rotten: {file.name}")
    
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    normalized = normalizer.normalize_dataset(data)
    
    output_file = NORM_DIR / f"normalized_{file.name}"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(normalized, f, indent=4, ensure_ascii=False)
        
    print(f"[OK] Rotten normalized saved -> {output_file}")
