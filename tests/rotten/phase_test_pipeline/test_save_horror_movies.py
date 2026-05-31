from pipeline.rotten import RottenPipeline


def test_save_rotten_horror_movies():

    BASES = {
        "movies_in_theaters": "movies_in_theaters",
        "movies_at_home": "movies_at_home",
        "movies_coming_soon": "movies_coming_soon",
        "movies_tv_shows": "tv_series_browse"
    }

    pipeline = RottenPipeline()

    try:
        pipeline.run(
            bases=BASES,
            max_pages=2
        )

        print("\n[OK] RAW ROTTEN PIPELINE DONE")

    finally:
        pipeline.close()


if __name__ == "__main__":
    test_save_rotten_horror_movies()