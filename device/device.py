#! /usr/bin/env python3
from fsm import FSM


class Device:

    def __init__(self, fsm=FSM()):
        self.__fsm = fsm
        self.__buffer = []

    def is_empty(self):
        return not len(self.__buffer)

        
