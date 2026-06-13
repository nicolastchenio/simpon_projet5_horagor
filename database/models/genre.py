from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database.base import Base

from database.models.associations import film_genre


class Genre(Base):

    __tablename__ = "genre"

    id_genre: Mapped[int] = mapped_column(
        primary_key=True
    )

    nom: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    films = relationship(
        "Film",
        secondary=film_genre,
        back_populates="genres"
    )