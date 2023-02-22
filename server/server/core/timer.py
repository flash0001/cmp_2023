#! /usr/bin/env python3
import asyncio
from datetime import datetime


class Timer:
    def __init__(self):
        self._start_at = None
        self._stop_at = None

    def start(self):
        if self._start_at is None:
            self._start_at = datetime.now().astimezone()
        return self._start_at

    @property
    def start_at(self):
        return self._start_at

    @property
    def stop_at(self):
        return self._stop_at

    @property
    def value(self):
        start = datetime.now().astimezone()
        stop = start
        if self._start_at is not None:
            start = self._start_at
        if self._stop_at is not None:
            stop = self._stop_at
        return stop - start

    def stop(self):
        if self._start_at is not None and self._stop_at is None:
            self._stop_at = datetime.now().astimezone()
        return [self._start_at, self._stop_at]

    def reset(self):
        self.__init__()


class CountdownTimer:
    __FunctionType = type(lambda _: _)

    def __init__(
        self,
        seconds,
        callback=lambda *args, **kwargs: (args, kwargs),
        *args,
        **kwargs,
    ):
        if isinstance(callback, CountdownTimer.__FunctionType):
            self.__callback = callback
            self.__args = args
            self.__kwargs = kwargs
            self.__return = None
        else:
            t = type(callback)
            raise TypeError(f"callback must be function, not {t}")
        self.__is_running = False
        self.__timer = Timer()
        if isinstance(seconds, int) and seconds > 0:
            self.__seconds = seconds
        elif isinstance(seconds, int) and seconds <= 0:
            raise ValueError(
                "value of seconds argument must be greater than 0 but ti is {seconds}"
            )
        else:
            t = type(seconds)
            raise TypeError(f"seconds must be int, not {t}")
        self.__seconds = seconds

    def is_running(self):
        return self.__is_running

    def start(self):
        if not self.__is_running:
            async def _():
                self.__is_running = True
                while self.__timer.value.seconds < self.__seconds:
                    pass
                self.__return = self.__callback(*self.__args, **self.__kwargs)
                self.__is_running = False
            asyncio.run(_())

    @property
    def result(self):
        return self.__return
