#! /usr/bin/env python3
"""FSM"""


class State:
    """Base state"""

    def __init__(self, fsm):
        self._fsm = fsm

    def __eq__(self, another_state):
        return self.STATE_NAME == another_state.STATE_NAME

    @property
    def name(self):
        return "undefined"

    def fsm(self):
        return self._fsm

    def is_free_state(self):
        return False

    def is_race_state(self):
        return False

    def is_finish_state(self):
        return False


class FreeState(State):

    STATE_NAME = "free"

    def next(self):
        # TODO check init data
        self._fsm.set_race_state()

    @property
    def name(self):
        return FreeState.STATE_NAME

    def is_free_state(self):
        return True


class RaceState(State):

    STATE_NAME = "race"

    def next(self):
        # TODO check time
        self._fsm.set_finish_state()

    @property
    def name(self):
        return RaceState.STATE_NAME

    def is_race_state(self):
        return True


class FinishState(State):

    STATE_NAME = "finish"

    def next(self):
        # TODO get race data
        self._fsm.set_free_state()
        # TODO return race data

    @property
    def name(self):
        return FinishState.STATE_NAME

    def is_finish_state(self):
        return True


class FSM:

    def __init__(self):
        self.__free_state = FreeState(self)
        self.__race_state = RaceState(self)
        self.__finish_state = FinishState(self)
        self.__current_state = self.__free_state

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
        self.__current_state.next()
