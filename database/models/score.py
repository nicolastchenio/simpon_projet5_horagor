from sqlalchemy import Numeric
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database.base import Base


class Score(Base):

    __tablename__ = "score"

    id_score: Mapped[int] = mapped_column(
        primary_key=True
    )

    score_tmdb: Mapped[float | None] = mapped_column(
        Numeric(3, 1)
    )

    score_imdb: Mapped[float | None] = mapped_column(
        Numeric(3, 1)
    )

    score_rotten_critics: Mapped[float | None] = mapped_column(
        Numeric(5, 2)
    )

    score_rotten_audience: Mapped[float | None] = mapped_column(
        Numeric(5, 2)
    )

    score_horragor: Mapped[float | None] = mapped_column(
        Numeric(3, 1)
    )

    id_film: Mapped[int] = mapped_column(
        ForeignKey(
            "film.id_film",
            ondelete="CASCADE"
        ),
        unique=True
    )

    film = relationship(
        "Film",
        back_populates="score"
    )