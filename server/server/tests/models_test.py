from ..server.models import Race, RaceType


def race_test(**data):
    try:
        race = Race(**data)
        print(race)
    except Exception as error:
        print(error)


race_test(race_type=RaceType.Qualifying, drivers=[])
