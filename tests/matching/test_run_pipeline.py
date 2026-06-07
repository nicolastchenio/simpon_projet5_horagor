# tests/matching/test_run_pipeline.py

from processing.matching.run import MatchingPipeline
from processing.normalization.schema import FilmNormalized, IDBlock


def run_test():
    """
    Test du pipeline complet MDM :
    - ID matching prioritaire
    - fuzzy matching fallback
    - typage Pydantic strict
    """

    pipeline = MatchingPipeline()

    # -----------------------------
    # DATA MOCK (FilmNormalized obligatoire)
    # -----------------------------
    tmdb_data = [
        FilmNormalized(ids=IDBlock(tmdb_id=1), title="Smile", release_year=2022),
        FilmNormalized(ids=IDBlock(tmdb_id=2), title="The Black Phone", release_year=2022),
        FilmNormalized(ids=IDBlock(tmdb_id=3), title="Orphan: First Kill", release_year=2022),
    ]

    kaggle_data = [
        # Match par ID
        FilmNormalized(ids=IDBlock(tmdb_id=1), title="Smile", release_year=2022),
        # Match Fuzzy
        FilmNormalized(ids=IDBlock(), title="The Black Phone", release_year=2022),
        # Pas de match
        FilmNormalized(ids=IDBlock(), title="Inexistant", release_year=2022),
    ]

    imdb_data = [
        # Match par ID
        FilmNormalized(ids=IDBlock(tmdb_id=2), title="The Black Phone", release_year=2022),
    ]
    
    rotten_data = [
        # Match Fuzzy
        FilmNormalized(ids=IDBlock(), title="Smile", release_year=2022),
    ]

    # -----------------------------
    # PIPELINE EXECUTION
    # -----------------------------
    results = pipeline.run(
        tmdb=tmdb_data,
        kaggle=kaggle_data,
        imdb=imdb_data,
        rotten=rotten_data,
    )

    # -----------------------------
    # OUTPUT DEBUG
    # -----------------------------
    print(f"MatchRecords générés : {len(results)}")

    for r in results:
        print(
            f"{r.master_id} | "
            f"TMDB={r.tmdb_index} | "
            f"INDICES={r.source_indices} | "
            f"LEVEL={r.match_level}"
        )

    # -----------------------------
    # ASSERTIONS
    # -----------------------------
    # On attend des matches pour Smile (0) et Black Phone (1)
    # Orphan (2) n'a pas de match dans les sources externes ici
    assert len(results) >= 2

    # Vérification Smile (TMDB index 0)
    smile_match = next(r for r in results if r.tmdb_index == 0)
    assert smile_match.source_indices["kaggle"] == 0
    assert smile_match.source_indices["rotten"] == 0
    assert "[ID_TMDB_KAGGLE]" in smile_match.match_level
    assert "[FUZZY_ROTTEN]" in smile_match.match_level

    # Vérification Black Phone (TMDB index 1)
    phone_match = next(r for r in results if r.tmdb_index == 1)
    assert phone_match.source_indices["kaggle"] == 1 # Fuzzy car pas d'ID dans kaggle_data[1]
    assert phone_match.source_indices["imdb"] == 0   # ID car présent dans imdb_data[0]
    assert "[ID_TMDB_IMDB]" in phone_match.match_level
    assert "[FUZZY_KAGGLE]" in phone_match.match_level

    print("\n[OK] Pipeline MDM fonctionnel (Agnostic + Prioritaire)")


if __name__ == "__main__":
    run_test()
