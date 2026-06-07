# tests/matching/test_id_matcher.py

import json
from processing.normalization.schema import FilmNormalized
from processing.matching.id_matcher import IDMatcher


TMDB_FILE = "data/normalized/tmdb/normalized_horror_page_1.json"
KAGGLE_FILE = "data/normalized/kaggle/normalized_kaggle.json"


def load_movies(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [FilmNormalized.model_validate(m) for m in data]


def main():
    print("Chargement des données...")
    tmdb_movies = load_movies(TMDB_FILE)
    kaggle_movies = load_movies(KAGGLE_FILE)

    matcher = IDMatcher()

    print("Matching par TMDB ID...")
    matches = matcher.match_by_tmdb_id(
        tmdb_movies=tmdb_movies,
        external_movies=kaggle_movies,
        source_name="kaggle"
    )

    print(f"\nTMDB films   : {len(tmdb_movies)}")
    print(f"Kaggle films : {len(kaggle_movies)}")
    print(f"Matches      : {len(matches)}")
    print("\n10 premiers matches :")

    for m in matches[:10]:
        print(
            f"{m.master_id} | "
            f"Level: {m.match_level} | "
            f"TMDB_idx: {m.tmdb_index} | "
            f"KAGGLE_idx: {m.source_indices.get('kaggle')}"
        )


if __name__ == "__main__":
    main()
