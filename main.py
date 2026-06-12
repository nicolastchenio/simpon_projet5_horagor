import sys
from pipeline.runner import main as run_ingestion

from processing.cleaning.tmdb.run import main as clean_tmdb
from processing.cleaning.rotten.run import main as clean_rotten
from processing.cleaning.kaggle.run import main as clean_kaggle
from processing.cleaning.imdb.run import main as clean_imdb

from processing.normalization.tmdb.run import main as normalize_tmdb
from processing.normalization.rotten.run import main as normalize_rotten
from processing.normalization.kaggle.run import main as normalize_kaggle
from processing.normalization.imdb.run import main as normalize_imdb

from processing.matching.run import main as run_matching
from processing.fusion.run import main as run_fusion
from processing.gold.run import main as generate_gold

def orchestrate(max_pages=None):
    """
    Orchestre l'ensemble du pipeline HorRAGor.
    """
    print("\n" + "="*50)
    print("      HORRAGOR - ORCHESTRATEUR CENTRAL")
    print("="*50 + "\n")

    # 1. INGESTION
    print("--- PHASE 1 : INGESTION ---")
    run_ingestion(max_pages=max_pages)

    # 2. NETTOYAGE
    print("\n--- PHASE 2 : NETTOYAGE (CLEANING) ---")
    clean_tmdb()
    clean_rotten()
    clean_kaggle()
    clean_imdb()

    # 3. NORMALISATION
    print("\n--- PHASE 3 : NORMALISATION ---")
    normalize_tmdb()
    normalize_rotten()
    normalize_kaggle()
    normalize_imdb()

    # 4. MATCHING
    print("\n--- PHASE 4 : MATCHING ---")
    run_matching()

    # 5. FUSION (MDM)
    print("\n--- PHASE 5 : FUSION ---")
    run_fusion()

    # 6. GOLD DATASET
    print("\n--- PHASE 6 : GÉNÉRATION GOLD DATASET ---")
    generate_gold()

    print("\n" + "="*50)
    print("   PROCESSUS TERMINÉ AVEC SUCCÈS")
    print("="*50 + "\n")

if __name__ == "__main__":
    # Par défaut, on peut passer le nombre de pages en argument
    # Exemple : uv run python main.py 10
    pages = None
    if len(sys.argv) > 1:
        try:
            pages = int(sys.argv[1])
        except ValueError:
            print(f"[WARN] Argument '{sys.argv[1]}' invalide, récupération de la totalité.")
    
    orchestrate(max_pages=pages)
