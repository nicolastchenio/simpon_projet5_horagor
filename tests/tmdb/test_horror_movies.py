from ingestion.tmdb_client import TMDBClient
import json

# Création du client TMDB
client = TMDBClient()

# Récupération des films d'horreur
data = client.get_horror_movies()

print("-------- response json du Premier film d'horreur -----------\n")
print(json.dumps(data["results"][0], indent=4, ensure_ascii=False))

print("-------- json liste des films d'horreur -----------\n")
print(json.dumps(data, indent=4, ensure_ascii=False))

print("--------  Films d'horreur récupérés avec succès -------- \n")

# Affichage des 5 premiers films
for movie in data.get("results", [])[:5]:

    print(f"ID : {movie.get('id')}")
    print(f"Titre : {movie.get('title')}")
    print(f"Date : {movie.get('release_date')}")
    print(f"Note : {movie.get('vote_average')}")
    print(f"Popularité : {movie.get('popularity')}")

    print("-" * 40)