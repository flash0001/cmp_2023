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
            "start_at": timer.start_at,
            "stop_at": timer.stop_at,
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
            self.__fsm.set_race_state()
            self.__fsm.next()

    @property
    def state(self):
        return self.__fsm.state
