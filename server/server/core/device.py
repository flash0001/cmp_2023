#! /usr/bin/env python3
if __name__ == "__main__":
    import json
    import sys
    from fsm import FSM
else:
    from .fsm import FSM


class Device:

    def __init__(self, fsm: FSM = FSM()):
        self.__fsm = fsm
        self.__driver_id = None
        self.__race_type = None

    def set(self, *, driver_id: int, race_type: str):
        if self.__fsm.state.is_free_state():
            self.__driver_id = driver_id
            self.__race_type = race_type

    def get(self):
        timer = self.__fsm.timer
        data = {
            "driver_id": self.__driver_id,
            "race_type": self.__race_type,
            "started_at": str(timer.started_at),
            "finished_at": str(timer.stopped_at),
            "duration": (timer.stopped_at - timer.started_at).seconds,
            "state": self.__fsm.state.name,
            "telemetry": [],
        }
        if self.__fsm.state.is_finish_state():
            data["telemetry"] = self.__fsm.buffer
        return data

    def reset(self):
        if self.__fsm.state.is_finish_state:
            self.__fsm.reset()
            self.__driver_id = None
            self.__race_type = None

    def run(self):
        if self.__fsm.state.is_free_state():
            self.__fsm.run_race()

    def stop(self):
        self.__fsm.set_finish_state()

    @property
    def state(self):
        return self.__fsm.state


if __name__ == "__main__":
    dev = Device()
    race_type, driver_id = sys.argv[1:3]
    dev.set(driver_id=driver_id, race_type=race_type)
    dev.run()
    sys.stdout.write(json.dumps(dev.get()))
    sys.exit(0)
