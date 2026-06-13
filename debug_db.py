from database.session import engine, SessionLocal
from sqlalchemy import text, inspect
from database.models import Film

def debug_db():
    print("--- Diagnostic Base de Données ---")
    
    # 1. Vérification de l'URL de connexion
    print(f"URL de connexion utilisée : {engine.url}")
    
    # 2. Vérification des tables via SQLAlchemy
    inspector = inspect(engine)
    tables = inspector.get_table_names(schema='public')
    print(f"Tables trouvées dans 'public' via SQLAlchemy : {tables}")
    
    # 3. Test de comptage si la table film existe
    if 'film' in tables:
        try:
            db = SessionLocal()
            count = db.query(Film).count()
            print(f"Nombre de films dans la table 'film' : {count}")
            db.close()
        except Exception as e:
            print(f"Erreur lors du comptage : {e}")
    else:
        print("La table 'film' n'existe pas dans le schéma 'public'.")

    # 4. Vérification de la base réelle via SQL
    with engine.connect() as conn:
        res = conn.execute(text("SELECT current_database(), current_user, inet_server_addr(), inet_server_port()"))
        db_info = res.fetchone()
        print(f"Base : {db_info[0]}")
        print(f"Utilisateur : {db_info[1]}")
        print(f"IP Serveur : {db_info[2]}")
        print(f"Port Serveur : {db_info[3]}")

if __name__ == "__main__":
    debug_db()
