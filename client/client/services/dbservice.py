from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, ForeignKey
import os
from pathlib import Path
import sqlalchemy as db
from sqlalchemy import text, ForeignKey
import sqlite3
from datetime import datetime

__dir__ = os.path.abspath(os.path.dirname(__file__))

DATABASE = f"{__dir__}/../../database.db"
SQL = f"{__dir__}/database.sql"


database_exists = os.path.isfile(DATABASE)

if not database_exists:
    with open(SQL) as fp:
        with sqlite3.connect(DATABASE) as connect:
            connect.executescript(fp.read())

engine = db.create_engine(f"sqlite:////{DATABASE}", echo=True)


# declarative base class
class Base(DeclarativeBase):
    pass


class Competition(Base):
    __tablename__ = "competition"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sponsor: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    race: Mapped[list["Race"]] = relationship(
        back_populates="competition", cascade="all, delete-orphan")


class Driver(Base):
    __tablename__ = "driver"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, default="")
    surname: Mapped[str] = mapped_column(nullable=False, default="")


class RaceType(Base):
    __tablename__ = "race_type"
    key: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    race: Mapped[list["Race"]] = relationship(
        back_populates="race_type",  cascade="all, delete-orphan")


class Race(Base):
    __tablename__ = "race"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    competition_id: Mapped[int] = mapped_column((ForeignKey("competition.id")))
    race_type: Mapped[str] = mapped_column((ForeignKey("key")))
    start_at: Mapped[str] = mapped_column(
        nullable=False,
        default=lambda: str(datetime.now().astimezone())
    )
    start_at: Mapped[str] = mapped_column(nullable=True)
    data: Mapped[str] = mapped_column(nullable=True)

    competition: Mapped[Competition.__name__] = relationship(
        back_populates="race")
    race_type: Mapped[RaceType.__name__] = relationship(back_populates="race")


class DriverHasRace(Base):
    __tablename__ = "driver_has_race"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
