from ingestion.tmdb_client import TMDBClient
import json

# Création du client TMDB
client = TMDBClient()

# Appel de la méthode qui récupère les genres
data = client.get_movie_genres()

print("-------- json liste des genres -----------\n")
print(json.dumps(data, indent=4, ensure_ascii=False))


print("----- Liste des genres TMDB ---------------\n")

# Parcours de chaque genre
for genre in data.get("genres", []):

    # Affichage de l'identifiant du genre
    print(f"ID : {genre.get('id')}")

    # Affichage du nom du genre
    print(f"Nom : {genre.get('name')}")

    print("-" * 30)