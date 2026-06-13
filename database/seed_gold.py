import json
from sqlalchemy.orm import Session
from database.session import SessionLocal, engine
from database.models import (
    Film, Score, Acteur, Genre, Realisateur, SocieteProduction
)

def get_or_create(session: Session, model, **kwargs):
    """
    Récupère une instance d'un modèle à partir de la base de données ou la crée si elle n'existe pas.

    Args:
        session (Session): La session SQLAlchemy active.
        model: La classe du modèle SQLAlchemy (ex: Genre, Acteur).
        **kwargs: Les attributs permettant de filtrer ou de créer l'instance (ex: nom="Horreur").

    Returns:
        L'instance récupérée ou nouvellement créée du modèle.
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        # On flush pour générer l'ID en base sans valider la transaction définitivement
        session.flush() 
        return instance

def seed_data(file_path: str):
    """
    Importe les données de films d'horreur depuis un fichier JSON "Gold" vers la base de données.

    Cette fonction assure la gestion des relations et gère les doublons potentiels 
    dans les listes de genres, d'acteurs ou de sociétés de production.

    Elle utilise des transactions pour garantir l'intégrité des données : en cas d'erreur, 
    tous les changements sont annulés (rollback).

    Args:
        file_path (str): Chemin vers le fichier JSON contenant les données fusionnées.
    """
    # Initialisation d'une session locale
    db: Session = SessionLocal()
    try:
        # Ouverture et lecture du fichier JSON source
        with open(file_path, "r", encoding="utf-8") as f:
            movies_data = json.load(f)

        total_movies = len(movies_data)
        print(f"Début de l'importation de {total_movies} films...")

        for index, item in enumerate(movies_data, 1):
            # 1. Gestion du réalisateur
            director_name = item.get("director") or "Inconnu"
            director = get_or_create(db, Realisateur, nom=director_name)

            # 2. Instanciation du film principal
            film = Film(
                titre=item.get("title"),
                annee_sortie=item.get("release_year"),
                langue_originale=item.get("original_language"),
                synopsis=item.get("overview"),
                tagline=item.get("tagline"),
                duree=item.get("runtime"),
                budget=item.get("budget"),
                revenue=item.get("revenue"),
                id_realisateur=director.id_realisateur
            )
            db.add(film)
            # Flush nécessaire pour obtenir l'id_film généré par la DB
            db.flush()

            # 3. Création de l'entrée Score associée au film
            score = Score(
                score_tmdb=item.get("score_tmdb"),
                score_imdb=item.get("score_imdb"),
                score_rotten_critics=item.get("score_rotten_critics"),
                score_rotten_audience=item.get("score_rotten_audience"),
                score_horragor=item.get("score_horragor"),
                id_film=film.id_film
            )
            db.add(score)

            # 4. Association des genres (Many-to-Many)
            genres_list = sorted(list(set(item.get("genres") or [])))
            for g_name in genres_list:
                genre = get_or_create(db, Genre, nom=g_name)
                film.genres.append(genre)

            # 5. Association des acteurs (Many-to-Many)
            cast_list = sorted(list(set(item.get("cast") or [])))
            for a_name in cast_list:
                acteur = get_or_create(db, Acteur, nom=a_name)
                film.acteurs.append(acteur)

            # 6. Association des sociétés de production (Many-to-Many)
            prod_list = sorted(list(set(item.get("production_companies") or [])))
            for p_name in prod_list:
                societe = get_or_create(db, SocieteProduction, nom=p_name)
                film.societes_production.append(societe)

            # Affichage de la progression tous les 100 films
            if index % 100 == 0 or index == total_movies:
                print(f"Progression : {index}/{total_movies} films traités...")

        # Validation de l'ensemble des opérations
        db.commit()
        print("Importation terminée avec succès !")

    except Exception as e:
        # Annulation complète en cas d'erreur durant le processus
        db.rollback()
        print(f"Erreur lors de l'importation : {e}")
        raise e
    finally:
        # Fermeture de la session
        db.close()

if __name__ == "__main__":
    # Exécution du script d'importation
    seed_data("data/gold/gold_horror_movies.json")
