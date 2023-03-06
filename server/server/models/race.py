from enum import Enum
from pydantic import BaseModel, Field, ValidationError


class RaceType(str, Enum):
    Qualifying = "qualifying"
    Top32 = "top_32"
    Top16 = "top_16"
    Top8 = "top_8"
    Semifinal = "semifinal"
    BattleFor3rdPlace = "battle for 3rd place"
    Final = "final"


class Race(BaseModel):
    race_type: RaceType
    drivers: list[int] = Field(ge=1, le=99, min_items=1, unique_items=True)
