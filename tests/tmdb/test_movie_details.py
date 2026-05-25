from ingestion.tmdb_client import TMDBClient
import json


# Création du client TMDB
client = TMDBClient()

# ID d'un film d'horreur récupéré précédemment
movie_id = 1304313

# Récupération des détails du film
data = client.get_movie_details(movie_id)

print("-------- JSON détail film -----------\n")

# Affichage JSON complet
print(json.dumps(data, indent=4, ensure_ascii=False))

print("\n-------- Informations importantes -----------\n")

# Affichage de quelques champs importants
print(f"ID : {data.get('id')}")
print(f"IMDB ID : {data.get('imdb_id')}")
print(f"Titre : {data.get('title')}")
print(f"Date : {data.get('release_date')}")
print(f"Durée : {data.get('runtime')} minutes")
print(f"Budget : {data.get('budget')}")
print(f"Revenue : {data.get('revenue')}")
print(f"Note : {data.get('vote_average')}")