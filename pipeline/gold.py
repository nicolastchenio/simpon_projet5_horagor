# pipeline/gold.py

import json
from pathlib import Path
from typing import List

from processing.normalization.schema import FilmNormalized
from processing.matching.run import MatchingPipeline
from processing.fusion.run import FusionPipeline


class GoldPipeline:
    """
    Pipeline final de génération du dataset GOLD.
    Réunit toutes les sources normalisées, les réconcilie et les fusionne.
    """

    def __init__(self):
        self.matching_pipeline = MatchingPipeline()
        self.fusion_pipeline = FusionPipeline()
        self.gold_dir = Path("data/gold")
        self.gold_dir.mkdir(parents=True, exist_ok=True)

    def load_normalized_data(self, dir_path: str) -> List[FilmNormalized]:
        """Charge tous les fichiers JSON normalisés d'un dossier."""
        data = []
        path = Path(dir_path)
        if not path.exists():
            print(f"⚠️ Dossier introuvable : {dir_path}")
            return []

        for file in path.glob("*.json"):
            print(f"Chargement {file.name}...")
            with open(file, "r", encoding="utf-8") as f:
                raw_list = json.load(f)
                data.extend([FilmNormalized.model_validate(m) for m in raw_list])
        
        return data

    def run(self):
        print("=== DÉMARRAGE DU PIPELINE GOLD ===\n")

        # 1. Chargement des données
        print("--- 1. Chargement des sources normalisées ---")
        tmdb_data = self.load_normalized_data("data/normalized/tmdb")
        kaggle_data = self.load_normalized_data("data/normalized/kaggle")
        imdb_data = self.load_normalized_data("data/normalized/imdb")
        rotten_data = self.load_normalized_data("data/normalized/rotten")

        print(f"\nVolumes chargés :")
        print(f"- TMDB   : {len(tmdb_data)}")
        print(f"- Kaggle : {len(kaggle_data)}")
        print(f"- IMDb   : {len(imdb_data)}")
        print(f"- Rotten : {len(rotten_data)}")

        # 2. Matching (Réconciliation)
        print("\n--- 2. Phase de Matching (Réconciliation) ---")
        matches = self.matching_pipeline.run(
            tmdb=tmdb_data,
            kaggle=kaggle_data,
            imdb=imdb_data,
            rotten=rotten_data
        )
        print(f"Matches identifiés : {len(matches)}")

        # 3. Fusion (Consolidation)
        print("\n--- 3. Phase de Fusion (Enrichissement) ---")
        gold_dataset = self.fusion_pipeline.run(
            matches=matches,
            tmdb_data=tmdb_data,
            kaggle_data=kaggle_data,
            imdb_data=imdb_data,
            rotten_data=rotten_data
        )
        print(f"Films dans le dataset Gold : {len(gold_dataset)}")

        # 4. Sauvegarde
        print("\n--- 4. Sauvegarde du dataset Gold ---")
        output_file = self.gold_dir / "horror_movies_gold.json"
        
        # Conversion Pydantic -> Dict pour JSON
        gold_json = [f.model_dump() for f in gold_dataset]
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(gold_json, f, indent=4, ensure_ascii=False)

        print(f"✅ Dataset GOLD sauvegardé avec succès : {output_file}")
        print("\n=== PIPELINE GOLD TERMINÉ ===")


if __name__ == "__main__":
    pipeline = GoldPipeline()
    pipeline.run()
