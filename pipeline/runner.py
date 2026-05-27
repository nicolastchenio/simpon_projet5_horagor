from pipeline.tmdb import TMDBPipeline
from pipeline.imdb import IMDbPipeline


def main():

    # =========================
    # TMDB
    # =========================

    tmdb_pipeline = TMDBPipeline()

    tmdb_pipeline.run(max_pages=3)

    # =========================
    # IMDb SQLite
    # =========================

    imdb_pipeline = IMDbPipeline()

    imdb_pipeline.run()


if __name__ == "__main__":
    main()