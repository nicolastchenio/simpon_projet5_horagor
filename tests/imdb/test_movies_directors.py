from ingestion.imdb_client import IMDbClient


# Initialisation du client IMDb
client = IMDbClient("data/raw/imdb/movie.sqlite")


print("\n=== FILMS + REALISATEURS ===\n")

# Récupération jointure SQL
results = client.fetch_movies_with_directors(limit=10)

# Affichage
for row in results:

    print(row)
    print("-" * 80)


# Fermeture connexion
client.close()