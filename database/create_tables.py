from database.base import Base
from database.session import engine

import database.models


def main():

    Base.metadata.create_all(bind=engine)

    print("Tables créées.")


if __name__ == "__main__":
    main()