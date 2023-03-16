from .timer import Timer
from .fsm import FSM


class Context(FSM):
    def __init__(self):
        super().__init__()
        self.__devices = []
        self.__timer = Timer()

    def is_run(self):
        pass

    def is_busy(self):
        return self.__timer.started_at() is not None and self.__timer.stopped_at() is None

    def is_free(self):
        return not bool(self.__devices)

    def is_complete(self):
        return self.__timer.stopped_at() is not None

    def add_device(self, device):
        self.__devices.append(device)

    async def run(self):
        m = map(lambda x: lambda: x.run(), self.__devices)
        self.__timer.run()
        await asyncio.gather(asyncio.to_thread(*m))
        self.__timer.stop()

    def get_data(self):
        data = {
            "started_at": self.__timer.started_at,
            "stopped_at": self.__timer.stopped_at,
            "data": [],
        }

        if data["stopped_at"] is not None:
            data["data"] = [*map(lambda d: d.get(), self.__devices)]

        return data

    def reset(self):
        if self.is_complete():
            self.__timer.reset()
            self.__devices = []
