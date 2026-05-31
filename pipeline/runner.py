from pipeline.tmdb import TMDBPipeline
from pipeline.imdb import IMDbPipeline
from pipeline.rotten import RottenPipeline


def main():

    # =========================
    # TMDB PIPELINE
    # =========================
    # tmdb_pipeline = TMDBPipeline()
    # tmdb_pipeline.run(max_pages=3)

    # =========================
    # IMDb PIPELINE
    # =========================
    # imdb_pipeline = IMDbPipeline()
    # imdb_pipeline.run()

    # =========================
    # ROTTEN PIPELINE (RAW SCRAPING)
    # =========================
    rotten_pipeline = RottenPipeline()

    try:
        for base in RottenPipeline.BASES.values():

            rotten_pipeline.run(
                base=base,
                max_pages=1  # <= contrôle global ici
            )

    finally:
        rotten_pipeline.close()


if __name__ == "__main__":
    main()