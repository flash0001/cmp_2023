import os
import sqlite3
from pathlib import Path
from typing import List
from datetime import datetime
import sqlalchemy as db
from sqlalchemy import select
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session as _Session
from sqlalchemy import Integer, String, ForeignKey, text

__dir__ = os.path.abspath(os.path.dirname(__file__))

DATABASE = f"{__dir__}/../../database.db"
SQL = f"{__dir__}/database.sql"


database_exists = os.path.isfile(DATABASE)

# if not database_exists:
#    with open(SQL) as fp:
#        with sqlite3.connect(DATABASE) as connect:
#            connect.executescript(fp.read())

engine = db.create_engine(f"sqlite:////{DATABASE}", echo=True)


# declarative base class
class Base(DeclarativeBase):
    pass


class Driver(Base):
    __tablename__ = "driver"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, default="")
    surname: Mapped[str] = mapped_column(nullable=False, default="")

    def __repr__(self) -> str:
        return f"Driver(id={self.id}, name={self.name}, surname={self.surname})"


class Competition(Base):
    __tablename__ = "competition"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sponsor: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    race: Mapped[List["Race"]] = relationship(
        back_populates="competition", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Competition(id={self.id}, sponsor={self.sponsor}, name={self.name})"


class RaceType(Base):
    __tablename__ = "race_type"
    key: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    # race: Mapped[List["Race"]] = relationship(back_populates="race_type", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"RaceType(key={self.key}, name={self.name})"


class Race(Base):
    __tablename__ = "race"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    competition_id: Mapped[int] = mapped_column(
        ForeignKey("competition.id"),
        nullable=False
    )
    race_type: Mapped[str] = mapped_column(
        ForeignKey("race_type.key"),
        nullable=False
    )
    start_at: Mapped[str] = mapped_column(
        nullable=False,
        default=lambda: str(datetime.now().astimezone())
    )
    stop_at: Mapped[str] = mapped_column(nullable=True)
    drivers: Mapped[str] = mapped_column(nullable=False)
    data: Mapped[str] = mapped_column(nullable=True)

    competition: Mapped[Competition.__name__] = relationship(
        back_populates="race"
    )

    # race_type: Mapped[RaceType.__name__] = relationship(back_populates="race")

    def __repr__(self) -> str:
        params = ", ".join([
            "id={self.id}",
            "competition_id={self.competition_id}",
            "race_type={self.race_type}",
            "start_at={self.start_at}",
            "stop_at={self.stop_at}",
            "data={self.data}",
        ])
        return f"Race({params})"

# class DriverHasRace(Base):
#    __tablename__ = "driver_has_race"

#    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


Base.metadata.create_all(engine)

if not database_exists:
    with _Session(engine) as session:
        keys = [
            "qualifying",
            "top 32",
            "top 16",
            "top 8",
            "semifinal",
            "battle for 3rd place",
            "final",
        ]
        rts = []
        for name in keys:
            key = name.replace(" ", "_")
            rts.append(RaceType(key=key, name=name))
        session.add_all(rts)
        drivers = []
        for i in range(1, 100):
            drivers.append(Driver(id=i, name="", surname=""))
        session.add_all(drivers)
        session.commit()


class Session(_Session):
    def __init__(self, *_, **__): super().__init__(engine)


__all__ = [
    Session.__name__,
    Competition.__name__,
    Driver.__name__,
    RaceType.__name__,
    Race.__name__,
    "engine",
    "select",
]
