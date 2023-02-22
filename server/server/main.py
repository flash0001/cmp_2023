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
