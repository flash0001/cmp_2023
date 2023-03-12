from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, ForeignKey
import os
from pathlib import Path
import sqlalchemy as db
from sqlalchemy import text, ForeignKey
import sqlite3

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


class Sponsor(Base):
    __tablename__ = "sponsor"

    id:  Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Competition(Base):
    __tablename__ = "competition"

    id:  Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Driver(Base):
    __tablename__ = "driver"
    id:  Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class RaceType(Base):
    __tablename__ = "race_type"
    key:  Mapped[str] = mapped_column(primary_key=True)


class Race(Base):
    __tablename__ = "race"

    id:  Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class DriverHasRace(Base):
    __tablename__ = "driver_has_race"

    id:  Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
