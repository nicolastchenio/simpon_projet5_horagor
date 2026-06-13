from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database.base import Base

from database.models.associations import film_acteur


class Acteur(Base):

    __tablename__ = "acteur"

    id_acteur: Mapped[int] = mapped_column(
        primary_key=True
    )

    nom: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    films = relationship(
        "Film",
        secondary=film_acteur,
        back_populates="acteurs"
    )