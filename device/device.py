#! /usr/bin/env python3
from timer import Timer
from time import sleep
from random import randint


class State:
    """Base state"""

    def __init__(self, fsm):
        self._fsm = fsm

    def __eq__(self, another_state):
        return self.STATE_NAME == another_state.STATE_NAME

    def next(self):
        return self._fsm.state

    @property
    def name(self):
        return "undefined"

    def is_free_state(self):
        return False

    def is_race_state(self):
        return False

    def is_finish_state(self):
        return False


class FreeState(State):

    STATE_NAME = "free"

    def next(self):
        self._fsm.set_race_state()
        return super().next()

    @property
    def name(self):
        return FreeState.STATE_NAME

    def is_free_state(self):
        return True


class RaceState(State):

    STATE_NAME = "race"

    def __init__(self, fsm):
        super().__init__(fsm)
        self.__timer = Timer()

    def next(self):
        self.__timer.start()
        while self.__timer.value.seconds <= 60:
            value = randint(-360, 360)
            self._fsm.push(value)
            sleep(0.1)
        self.__timer.stop()
        self.__timer.reset()
        self._fsm.set_finish_state()
        return super().next()

    @property
    def name(self):
        return RaceState.STATE_NAME

    def is_race_state(self):
        return True


class FinishState(State):

    STATE_NAME = "finish"

    def next(self):
        self._fsm.reset()
        self._fsm.set_free_state()
        return super().next()

    @property
    def name(self):
        return FinishState.STATE_NAME

    def is_finish_state(self):
        return True


class Device:

    def __init__(self):
        self.__free_state = FreeState(self)
        self.__race_state = RaceState(self)
        self.__finish_state = FinishState(self)
        self.__current_state = self.__free_state
        self.__buffer = []

    @property
    def buffer(self):
        return tuple(self.__buffer)

    def push(self, value):
        self.__buffer.append(value)

    def reset(self):
        self.__buffer = []

    def set_free_state(self):
        self.__current_state = self.__free_state

    def set_race_state(self):
        self.__current_state = self.__race_state

    def set_finish_state(self):
        self.__current_state = self.__finish_state

    def is_free_state(self):
        return self.__current_state.is_free_state()

    def is_race_state(self):
        return self.__current_state.is_race_state()

    def is_finish_state(self):
        return self.__current_state.is_finish_state()

    @property
    def state(self):
        return self.__current_state

    def next(self):
        return self.__current_state.next()
