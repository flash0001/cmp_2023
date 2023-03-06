#! /usr/bin/env python3
from time import time
from datetime import datetime
import asyncio
from websockets import serve
from timer import Timer


class BaseState:
    def __init__(self, fsm):
        self._fsm = fsm


class WaitingForRaceSate(fsm):
    pass


class RaceState(fsm):
    pass


class FinishedRaceState(fsm):
    pass


class FiniteStateMachine:
    def __init__(self):
        self._wrs = WaitingForRaceSate(self)
        self._rs = RaceState(self)
        self._frs = FinishedRaceState(self)
        self._current = self._wrs
        self._timer = Timer()


async def handler(websocket):
    while True:
        try:
            message = await websocket.recv()
        except websockets.ConnectionClosedOK:
            break

    async for message in websocket:
        await websocket.send(message)


async def countdown(websocket):
    start = datetime.now().astimezone()
    async for i in range(60):
        await websocket.send({"race": str(i+1), })
        sleep(1)


async def main():
    async with serve(handler, "", 1024):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())


def validate_driver_id(idx: int):
    if not isinstance(idx, int):
        raise ClientError(f"driver_id must be int, but type is {type(idx)}")
    elif idx < 1 or idx > 99:
        raise ClientError("value of driver_id out of range")


def validate_race_type(race_type):
    if not isinstance(race_type, str):
        raise ClientError(
            f"race_type must be str, but type is {type(race_type)}")
    if race_type not in RACE_TYPE:
        raise ClientError("unknown type of race")


def validate_user_data(data):
    if not isinstance(data, list):
        raise ClientError(f"data must be list, but received {type(data)}")
    for item in data:
        validate_driver_id(item.get("driver_id"))
        validate_race_type(item.get("race_type"))
