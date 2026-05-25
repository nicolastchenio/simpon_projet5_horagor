from ingestion.tmdb_client import TMDBClient
import json
from pathlib import Path


# Création du client TMDB
client = TMDBClient()

# Récupération des films d'horreur
data = client.get_horror_movies(page=1)

# Création du chemin du dossier de sauvegarde
output_dir = Path("data/raw/tmdb")

# Création du fichier de sortie
output_file = output_dir / "horror_movies_page_1.json"

# Sauvegarde des données JSON
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("Fichier JSON sauvegardé avec succès")
print(f"Chemin : {output_file}")