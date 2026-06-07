# tests/matching/test_fuzzy_matcher.py

from processing.matching.fuzzy_matcher import FuzzyMatcher


def run_test():
    matcher = FuzzyMatcher()

    # -----------------------------
    # MOCK DATASETS
    # -----------------------------
    tmdb_data = [
        {
            "title": "The Black Phone",
            "release_date": "2022-06-22",
        },
        {
            "title": "Smile",
            "release_date": "2022-09-23",
        },
        {
            "title": "L'Étrange Noël de Monsieur Jack",
            "release_date": "1993-10-29",
        },
    ]

    kaggle_data = [
        {
            "title": "The Black Phone",
            "release_date": "2022-06-22",
        },
        {
            "title": "Smile",
            "release_date": "2022-09-23",
        },
        {
            "title": "The Nightmare Before Christmas",  # volontairement différent
            "release_date": "1993-10-29",
        },
    ]

    # -----------------------------
    # MATCHING
    # -----------------------------
    matches = matcher.match_all(tmdb_data, kaggle_data)

    print("Matches trouvés :", len(matches))

    for i, j in matches:
        print(
            f"✔ TMDB[{i}] -> Kaggle[{j}] | "
            f"{tmdb_data[i]['title']} ↔ {kaggle_data[j]['title']}"
        )

    # -----------------------------
    # ASSERTIONS MINIMALES
    # -----------------------------
    assert len(matches) >= 2, "Au moins 2 matches attendus"

    # vérifie que Black Phone match
    assert (0, 0) in matches

    # vérifie que Smile match
    assert (1, 1) in matches

    print("\n[OK] Fuzzy matcher fonctionne correctement")


if __name__ == "__main__":
    run_test()