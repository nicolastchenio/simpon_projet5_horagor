from ingestion.tmdb_client import TMDBClient
import json

client = TMDBClient()

data = client.get_popular_movies()

print("Connexion API réussie\n")

# Afficher le premier film complet
first_movie = data["results"][0]

print("-------- json du Premier film -----------\n")
print(json.dumps(first_movie, indent=4, ensure_ascii=False))

print("\n ---------------- Affichage des 5 premiers films populaires -------------\n")

for movie in data.get("results", [])[:5]:
    print(f"id : {movie.get('id')}")
    print(f"Titre : {movie.get('title')}")
    print(f"Date : {movie.get('release_date')}")
    print(f"Note : {movie.get('vote_average')}")
    print("-" * 40)
    
