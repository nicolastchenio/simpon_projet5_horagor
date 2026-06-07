# tests/matching/test_run_pipeline.py

from processing.matching.run import MatchingPipeline
from processing.normalization.schema import FilmNormalized


def run_test():
    """
    Test du pipeline MDM complet.

    Objectif :
    - vérifier matching ID + fuzzy
    - vérifier cohérence TMDB comme master
    """

    pipeline = MatchingPipeline()

    # --------------------------------------------------
    # TMDB (MASTER DATA)
    # --------------------------------------------------
    tmdb_data = [
        FilmNormalized(
            ids={"tmdb_id": 1, "imdb_id": None},
            title="Smile",
            release_date="2022-09-23",
        ),
        FilmNormalized(
            ids={"tmdb_id": 2, "imdb_id": None},
            title="The Black Phone",
            release_date="2022-06-22",
        ),
        FilmNormalized(
            ids={"tmdb_id": 3, "imdb_id": None},
            title="Orphan: First Kill",
            release_date="2022-07-27",
        ),
    ]

    # --------------------------------------------------
    # KAGGLE DATA
    # --------------------------------------------------
    kaggle_data = [
        FilmNormalized(
            ids={"tmdb_id": 1, "imdb_id": None},
            title="Smile",
            release_date="2022-09-23",
        ),
        FilmNormalized(
            ids={"tmdb_id": 2, "imdb_id": None},
            title="The Black Phone",
            release_date="2022-06-22",
        ),
        FilmNormalized(
            ids={"tmdb_id": 3, "imdb_id": None},
            title="Orphan: First Kill",
            release_date="2022-07-27",
        ),
    ]

    # --------------------------------------------------
    # IMDB DATA (pas de tmdb_id → fuzzy only)
    # --------------------------------------------------
    imdb_data = [
        FilmNormalized(
            ids={"tmdb_id": None, "imdb_id": None},
            title="Smile",
            release_date="2022-09-23",
        ),
        FilmNormalized(
            ids={"tmdb_id": None, "imdb_id": None},
            title="The Black Phone",
            release_date="2022-06-22",
        ),
        FilmNormalized(
            ids={"tmdb_id": None, "imdb_id": None},
            title="Orphan: First Kill",
            release_date="2022-07-27",
        ),
    ]

    # --------------------------------------------------
    # ROTTEN DATA (idem IMDb)
    # --------------------------------------------------
    rotten_data = [
        FilmNormalized(
            ids={"tmdb_id": None, "imdb_id": None},
            title="Smile",
            release_date="2022-09-23",
        ),
        FilmNormalized(
            ids={"tmdb_id": None, "imdb_id": None},
            title="The Black Phone",
            release_date="2022-06-22",
        ),
        FilmNormalized(
            ids={"tmdb_id": None, "imdb_id": None},
            title="Orphan: First Kill",
            release_date="2022-07-27",
        ),
    ]

    # --------------------------------------------------
    # RUN PIPELINE MDM
    # --------------------------------------------------
    results = pipeline.run(
        tmdb_data,
        kaggle_data,
        imdb_data,
        rotten_data,
    )

    # --------------------------------------------------
    # OUTPUT
    # --------------------------------------------------
    print("MatchRecords générés :", len(results))

    for r in results:
        print(
            f"{r.master_id} | "
            f"TMDB={r.tmdb_index} | "
            f"KAGGLE={r.kaggle_index} | "
            f"IMDB={r.imdb_index} | "
            f"ROTTEN={r.rotten_index} | "
            f"LEVEL={r.match_level}"
        )

    # --------------------------------------------------
    # ASSERTIONS
    # --------------------------------------------------
    assert len(results) == 3, "MDM doit produire 3 entités TMDB"
    assert all(r.tmdb_index is not None for r in results)

    print("\n[OK] Pipeline MDM fonctionnel")


if __name__ == "__main__":
    run_test()
