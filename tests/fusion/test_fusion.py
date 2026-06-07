# tests/fusion/test_fusion.py

from processing.matching.run import MatchingPipeline
from processing.fusion.run import FusionPipeline
from processing.normalization.schema import FilmNormalized, IDBlock


def run_test():

    # --------------------------------------------------
    # 1. DATA MOCK (FilmNormalized)
    # --------------------------------------------------
    tmdb_data = [
        FilmNormalized(
            ids=IDBlock(tmdb_id=1, imdb_id="tt01"), 
            title="Smile", 
            release_year=2022,
            overview=None, # Manquant dans TMDB
            tagline="TMDB Tagline",
            genres=["Horreur"]
        ),
        FilmNormalized(
            ids=IDBlock(tmdb_id=2, imdb_id="tt02"), 
            title="The Black Phone", 
            release_year=2022,
            overview="TMDB Overview",
            runtime_minutes=None # Manquant dans TMDB
        ),
    ]

    kaggle_data = [
        FilmNormalized(
            ids=IDBlock(tmdb_id=1), 
            title="Smile", 
            release_year=2022,
            overview="Kaggle Overview for Smile", # Fallback priority 2
            genres=["Thriller"]
        ),
    ]

    imdb_data = [
        FilmNormalized(
            ids=IDBlock(imdb_id="tt02"), 
            title="The Black Phone", 
            release_year=2022,
            runtime_minutes=103 # Fallback priority 3
        ),
    ]

    rotten_data = [
        FilmNormalized(
            ids=IDBlock(), 
            title="Smile", 
            release_year=2022,
            overview="Rotten Overview for Smile", # Fallback priority 1
            genres=["Mystery"]
        ),
    ]

    # --------------------------------------------------
    # 2. MATCHING
    # --------------------------------------------------
    matcher = MatchingPipeline()

    matches = matcher.run(
        tmdb=tmdb_data,
        kaggle=kaggle_data,
        imdb=imdb_data,
        rotten=rotten_data,
    )

    print("\n--- MATCHING RESULT ---")
    print("MatchRecords générés :", len(matches))

    # --------------------------------------------------
    # 3. FUSION
    # --------------------------------------------------
    fusion_pipeline = FusionPipeline()

    films = fusion_pipeline.run(
        matches, 
        tmdb_data,
        kaggle_data=kaggle_data,
        imdb_data=imdb_data,
        rotten_data=rotten_data
    )

    print("\n--- FUSION RESULT ---")
    print("Films fusionnés :", len(films))

    for f in films:
        print(
            f"{f.master_id} | "
            f"title={f.title} | "
            f"sources={f.sources} | "
            f"overview={f.overview[:30]}... | "
            f"runtime={f.runtime_minutes} | "
            f"genres={f.genres}"
        )

    # --------------------------------------------------
    # 4. ASSERTIONS
    # --------------------------------------------------
    assert len(films) == 2
    
    # Smile : overview doit venir de Rotten (priorité 1) et genres = Union
    smile = next(f for f in films if f.tmdb_id == 1)
    assert "rotten" in smile.sources
    assert smile.overview == "Rotten Overview for Smile"
    assert "Horreur" in smile.genres
    assert "Mystery" in smile.genres
    assert "Thriller" in smile.genres

    # Black Phone : runtime doit venir de IMDb (priorité 3 car absent TMDB/Kaggle/Rotten)
    phone = next(f for f in films if f.tmdb_id == 2)
    assert "imdb" in phone.sources
    assert phone.overview == "TMDB Overview"
    assert phone.runtime_minutes == 103

    print("\n[OK] Fusion MDM Agnostique OK")


if __name__ == "__main__":
    run_test()
