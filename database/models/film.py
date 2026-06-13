from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import BigInteger
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database.base import Base

from database.models.associations import film_acteur
from database.models.associations import film_genre
from database.models.associations import film_societe_production


class Film(Base):

    __tablename__ = "film"

    id_film: Mapped[int] = mapped_column(
        primary_key=True
    )

    titre: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    annee_sortie: Mapped[int | None]

    langue_originale: Mapped[str | None] = mapped_column(
        String(10)
    )

    synopsis: Mapped[str | None] = mapped_column(
        Text
    )

    tagline: Mapped[str | None] = mapped_column(
        Text
    )

    duree: Mapped[int | None]

    budget: Mapped[int | None] = mapped_column(
        BigInteger
    )

    revenue: Mapped[int | None] = mapped_column(
        BigInteger
    )

    id_realisateur: Mapped[int] = mapped_column(
        ForeignKey("realisateur.id_realisateur")
    )

    realisateur: Mapped["Realisateur"] = relationship(
        back_populates="films"
    )

    score = relationship(
        "Score",
        back_populates="film",
        uselist=False
    )

    acteurs = relationship(
        "Acteur",
        secondary=film_acteur,
        back_populates="films"
    )

    genres = relationship(
        "Genre",
        secondary=film_genre,
        back_populates="films"
    )

    societes_production = relationship(
        "SocieteProduction",
        secondary=film_societe_production,
        back_populates="films"
    )