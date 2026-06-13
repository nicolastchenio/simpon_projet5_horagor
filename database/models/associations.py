from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import ForeignKey

from database.base import Base


film_acteur = Table(
    "film_acteur",
    Base.metadata,

    Column(
        "id_film",
        ForeignKey("film.id_film", ondelete="CASCADE"),
        primary_key=True
    ),

    Column(
        "id_acteur",
        ForeignKey("acteur.id_acteur", ondelete="CASCADE"),
        primary_key=True
    )
)

film_genre = Table(
    "film_genre",
    Base.metadata,

    Column(
        "id_film",
        ForeignKey("film.id_film", ondelete="CASCADE"),
        primary_key=True
    ),

    Column(
        "id_genre",
        ForeignKey("genre.id_genre", ondelete="CASCADE"),
        primary_key=True
    )
)

film_societe_production = Table(
    "film_societe_production",
    Base.metadata,

    Column(
        "id_film",
        ForeignKey("film.id_film", ondelete="CASCADE"),
        primary_key=True
    ),

    Column(
        "id_societe",
        ForeignKey(
            "societe_production.id_societe",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
)