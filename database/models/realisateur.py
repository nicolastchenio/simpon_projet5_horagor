from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database.base import Base


class Realisateur(Base):

    __tablename__ = "realisateur"

    id_realisateur: Mapped[int] = mapped_column(
        primary_key=True
    )

    nom: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True
    )

    films = relationship(
        "Film",
        back_populates="realisateur"
    )