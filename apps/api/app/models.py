#apps/api/app/models.py
from __future__ import annotations

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bgg_id: Mapped[int] = mapped_column(unique=True, index=True)
    name: Mapped[str]
    year_published: Mapped[int | None]
    thumbnail_url: Mapped[str | None]
    image_url: Mapped[str | None]

    placements: Mapped[list["Placement"]] = relationship(back_populates="game")


class Fixture(Base):
    __tablename__ = "fixtures"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    rows: Mapped[int]
    cols: Mapped[int]

    placements: Mapped[list["Placement"]] = relationship(back_populates="fixture")


class Placement(Base):
    __tablename__ = "placements"
    __table_args__ = (
        UniqueConstraint("fixture_id", "slot", name="uq_fixture_slot"),
        UniqueConstraint("game_id", name="uq_game_one_location"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fixture_id: Mapped[int] = mapped_column(ForeignKey("fixtures.id", ondelete="CASCADE"), index=True)
    slot: Mapped[str] = mapped_column(index=True)  # e.g. "r0c0"
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"), index=True)

    fixture: Mapped["Fixture"] = relationship(back_populates="placements")
    game: Mapped["Game"] = relationship(back_populates="placements")
