from pipeline.tmdb_pipeline import TMDBPipeline


def main():
    """
    Point d'entrée principal du projet.
    Lance les pipelines d'ingestion.
    """

    tmdb_pipeline = TMDBPipeline()

    # Test ingestion TMDB Horror
    tmdb_pipeline.run(max_pages=3)


if __name__ == "__main__":
    main()