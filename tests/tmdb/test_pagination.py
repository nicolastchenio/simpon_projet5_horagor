from ingestion.tmdb_client import TMDBClient


# Création du client TMDB
client = TMDBClient()

# Récupération de la première page des films Horror
data = client.get_horror_movies(page=1)

print("-------- Informations pagination -----------\n")

# Page actuelle
print(f"Page actuelle : {data.get('page')}")

# Nombre total de pages
print(f"Nombre total de pages : {data.get('total_pages')}")

# Nombre total de résultats
print(f"Nombre total de films : {data.get('total_results')}")

# Nombre de films dans cette page
print(f"Films dans cette page : {len(data.get('results', []))}")