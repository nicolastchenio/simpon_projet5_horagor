from database.session import engine
from sqlalchemy import text

def find_all_tables():
    with engine.connect() as conn:
        query = text("""
            SELECT table_schema, table_name 
            FROM information_schema.tables 
            WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
        """)
        result = conn.execute(query)
        tables = result.fetchall()
        print("--- Liste de toutes les tables (hors système) ---")
        for schema, name in tables:
            print(f"Schéma: {schema} | Table: {name}")
        if not tables:
            print("Aucune table trouvée.")

if __name__ == "__main__":
    find_all_tables()
