from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database.base import Base

from database.models.associations import film_societe_production


class SocieteProduction(Base):

    __tablename__ = "societe_production"

    id_societe: Mapped[int] = mapped_column(
        primary_key=True
    )

    nom: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True
    )

    films = relationship(
        "Film",
        secondary=film_societe_production,
        back_populates="societes_production"
    )