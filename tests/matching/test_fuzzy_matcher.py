# tests/matching/test_fuzzy_matcher.py

from processing.matching.fuzzy_matcher import FuzzyMatcher
from processing.normalization.schema import FilmNormalized, IDBlock


def run_test():
    matcher = FuzzyMatcher()

    # -----------------------------
    # MOCK DATASETS (FilmNormalized)
    # -----------------------------
    tmdb_data = [
        FilmNormalized(ids=IDBlock(), title="The Black Phone", release_year=2022),
        FilmNormalized(ids=IDBlock(), title="Smile", release_year=2022),
        FilmNormalized(ids=IDBlock(), title="L'Étrange Noël de Monsieur Jack", release_year=1993),
    ]

    kaggle_data = [
        FilmNormalized(ids=IDBlock(), title="The Black Phone", release_year=2022),
        FilmNormalized(ids=IDBlock(), title="Smile", release_year=2022),
        FilmNormalized(ids=IDBlock(), title="The Nightmare Before Christmas", release_year=1993),
    ]

    # -----------------------------
    # MATCHING
    # -----------------------------
    results = matcher.match(tmdb_data, kaggle_data, source_name="kaggle")

    print(f"Matches trouvés : {len(results)}")

    for r in results:
        tmdb_idx = r.tmdb_index
        ext_idx = r.source_indices["kaggle"]
        print(
            f"✔ {r.master_id} | TMDB[{tmdb_idx}] -> Kaggle[{ext_idx}] | "
            f"{tmdb_data[tmdb_idx].title} ↔ {kaggle_data[ext_idx].title}"
        )

    # -----------------------------
    # ASSERTIONS
    # -----------------------------
    assert len(results) >= 2, "Au moins 2 matches attendus"

    # Vérifie que Black Phone match (index 0 -> index 0)
    assert any(r.tmdb_index == 0 and r.source_indices["kaggle"] == 0 for r in results)

    # Vérifie que Smile match (index 1 -> index 1)
    assert any(r.tmdb_index == 1 and r.source_indices["kaggle"] == 1 for r in results)

    print("\n[OK] Fuzzy matcher fonctionne correctement")


if __name__ == "__main__":
    run_test()
