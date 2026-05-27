from ingestion.imdb_client import IMDbClient


# Initialisation du client
client = IMDbClient("data/raw/imdb/movie.sqlite")


print("\n=== ANALYSE QUALITE DES DONNEES IMDb ===\n")


# =====================================================
# NULL VALUES
# =====================================================

print("=== NULL VALUES ===\n")

nulls = client.analyze_null_values()

for key, value in nulls.items():
    print(f"{key}: {value}")

print("\n" + "=" * 80 + "\n")


# =====================================================
# DOUBLONS
# =====================================================

print("=== DOUBLONS ===\n")

duplicates = client.analyze_duplicates()

if duplicates:

    for row in duplicates[:10]:
        print(row)

else:
    print("Aucun doublon détecté.")

print("\n" + "=" * 80 + "\n")


# =====================================================
# DATES INVALIDES
# =====================================================

print("=== DATES INVALIDES ===\n")

invalid_dates = client.analyze_invalid_dates()

if invalid_dates:

    for row in invalid_dates[:10]:
        print(row)

else:
    print("Aucune date invalide.")

print("\n" + "=" * 80 + "\n")


# =====================================================
# DIFFERENCES TITLE / ORIGINAL_TITLE
# =====================================================

print("=== TITLE VS ORIGINAL_TITLE ===\n")

title_diff = client.analyze_title_differences()

if title_diff:

    for row in title_diff:
        print(row)

else:
    print("Aucune différence détectée.")

print("\n" + "=" * 80 + "\n")


# Fermeture connexion
client.close()