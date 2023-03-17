import os
import json
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
from sqlalchemy.orm import Session
from sqlalchemy import Integer, String, ForeignKey, text
#from .result import Result
from pathlib import Path


__dir__ = os.path.abspath(os.path.dirname(__file__))

DATABASE = ((Path(__dir__) / "..") / "..") / "database.db"
SQL = Path(__dir__) / "database.sql"


database_exists = os.path.isfile(DATABASE)

engine = db.create_engine(f"sqlite:////{DATABASE}", echo=True, connect_args={'timeout': 15})


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
    name: Mapped[str] = mapped_column(nullable=False)
    sponsor: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)

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
    )#    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    race_type: Mapped[str] = mapped_column(
        ForeignKey("race_type.key"),
        nullable=False
    )
    started_at: Mapped[str] = mapped_column(
        nullable=False,
        default=lambda: str(datetime.now().astimezone())
    )
    finished_at: Mapped[str] = mapped_column(nullable=True)
    drivers: Mapped[str] = mapped_column(nullable=False)
    telemetry: Mapped[str] = mapped_column(nullable=True)

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


def __insert_data():
    if not database_exists:
        with Session(engine) as session:
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


def __create_tables():
    Base.metadata.create_all(engine)
    __insert_data()


def get_race_type_names() -> list[str]:
    data = []
    with Session(engine) as session:
        for rec in session.scalars(select(RaceType)):
            data.append(rec.name)
    return data

def get_drivers_id() -> list[int]:
    data = []
    with Session(engine) as session:
        for rec in session.scalars(select(Driver)):
            data.append(rec.id)
    return data

def does_competition_exist() -> bool:
    return get_current_competition() is not None


def save_competition(*, name, sponsor, date, location):
    with Session(engine) as session:
        comp = Competition(
            name=name,
            sponsor=sponsor,
            date=date,
            location=location,
        )
        session.add_all([comp])
        session.commit()

def get_current_competition() -> Competition | None:
    with Session(engine) as session:
        out = None
        collections = session.scalars(select(Competition))
        for rec in collections:
            out = rec
            break
        return out

def get_races() -> list[Race]:
    with Session(engine) as session:
        data = []
        for rec in session.scalars(select(Race)):
            data.append(rec)
    return data

def make_archive():
    if does_competition_exist():
        comp = get_current_competition()
        races = get_races()
        with Session(engine) as session:
            pass

def save_race_results(data):
    print("[INFO] trying to save data into the database")
    if data:
        started_at = data[0]["started_at"]
        finished_at = data[0]["finished_at"]
        race_type = data[0]["race_type"]
        drivers = []
        telemetry = []
        for d in data:
            drivers.append(d["driver_id"])
            telemetry.append({
                "driver_id": d["driver_id"],
                "telemetry": d["telemetry"]
            })
        competition = get_current_competition()
        with _Session(engine) as session:
            race = Race(
                competition_id=competition.id,
                race_type=race_type,
                started_at=started_at,
                finished_at=finished_at,
                drivers=json.dumps(drivers),
                telemetry=json.dumps(telemetry),
            )
            race = session.add_all([race])
            session.commit()
            print("[INFO] the new race has been saved")
    else:
        print("[ERROR] empty data")


__create_tables()

__all__ = [
    "engine",
    "select",
    Driver.__name__,
    Competition.__name__,
    Race.__name__,
    RaceType.__name__,
    Session.__name__,
]


if __name__ == "__main__":
    print("COMPETITIONS: ", get_current_competition())
    print("RACE TYPES: ", get_race_type_names())
    print("DRIVERS: ", get_drivers_id())
