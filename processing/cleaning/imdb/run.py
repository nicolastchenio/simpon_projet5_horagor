# processing/cleaning/imdb/run.py

import json
from pathlib import Path
from processing.cleaning.imdb.cleaner import IMDBCLeaner


RAW_DIR = Path("data/raw/imdb")
CLEAN_DIR = Path("data/cleaned/imdb")

def main():
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)

    cleaner = IMDBCLeaner()

    for file in RAW_DIR.glob("imdb_movies*.json"):

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        cleaned = cleaner.clean_dataset(data)

        output_file = CLEAN_DIR / f"cleaned_{file.name}"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(cleaned, f, indent=4, ensure_ascii=False)

        print(f"[OK] IMDb cleaned saved -> {output_file}")

if __name__ == "__main__":
    main()
