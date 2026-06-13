from database.base import Base
from database.session import engine

import database.models


def main():
    print(f"Connexion à : {engine.url}")
    print("Métadonnées détectées :", Base.metadata.tables.keys())
    Base.metadata.create_all(bind=engine)
    print("Tables créées.")


if __name__ == "__main__":
    main()