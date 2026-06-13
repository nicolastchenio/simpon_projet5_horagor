from database.session import engine
from sqlalchemy import inspect, text

def check_db():
    inspector = inspect(engine)
    schemas = inspector.get_schema_names()
    print(f"Schémas trouvés : {schemas}")
    
    for schema in schemas:
        tables = inspector.get_table_names(schema=schema)
        if tables:
            print(f"Tables dans le schéma '{schema}' : {tables}")
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT current_database(), current_user, current_schema()"))
        row = result.fetchone()
        print(f"Connecté à la base : {row[0]} en tant que : {row[1]} (Schéma actuel : {row[2]})")

if __name__ == "__main__":
    check_db()

if __name__ == "__main__":
    check_db()
