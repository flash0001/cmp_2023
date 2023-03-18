import json
import os
import signal
from subprocess import Popen, PIPE
import sys
import time
from uuid import uuid4
from .timer import Timer


class Pout(dict):
    def __init__(self, stdout: bytes, stderr: bytes):
        super().__init__()
        self["stdout"] = self.decode(stdout)
        self["stderr"] = self.decode(stderr)

    def decode(self, data):
        return data.decode() if type(data) == bytes else data

    @property
    def stdout(self):
        return self["stdout"]

    @property
    def stderr(self):
        return self["stderr"]

    def __str__(self) -> str:
        return f"stdout: {self.stdout}\nstderr: {self.stderr}"

    def __repr__(self) -> str:
        return str(self)


class ProcessWrapper:

    def __init__(self, cmd, race_type, driver_id, data_dir):
        self.__timer = Timer()
        self.uuid = uuid4()
        self.file_path = f"{data_dir}/{self.uuid}"
        driver_id = str(driver_id)
        self.driver_id = driver_id
        self.race_type = race_type
        self.__timer.start()
        self.proc = Popen([
            sys.executable,
            cmd,
            race_type,
            driver_id,
            self.file_path
        ],
            stdout=PIPE,
            stderr=PIPE
        )

    def terminate(self):
        self.proc.terminate()
        self.__timer.stop()

    def send_signal(self, sig):
        self.proc.send_signal(sig)
        self.__timer.stop()

    def kill(self):
        self.proc.kill()
        self.__timer.stop()

    def communicate(self):
        data = {
            "started_at": str(self.__timer.started_at),
            "finished_at": str(self.__timer.stopped_at),
            "duration": str(self.__timer.duration.seconds),
            "race_type": self.race_type,
            "driver_id": self.driver_id,
            "telemetry": []
        }

        with open(self.file_path) as fp:
            raw = fp.read()[:-1]
            telemetry = [*map(lambda x: int(x), raw.split(","))]
            data["telemetry"] = telemetry
        return json.dumps(data), ""

    def __del__(self):
        os.remove(self.file_path)


class ProcPool:

    def __init__(self):
        self.__proc_list = []

    def add(self, cmd: str, race_type: str, driver_id, data_dir: str):
        proc = ProcessWrapper(cmd, race_type, driver_id, data_dir)
        self.__proc_list.append(proc)

    def stop(self) -> list[Pout]:
        out = []
        while len(self.__proc_list):
            proc = self.__proc_list.pop()
            if sys.platform == "win32":
                proc.terminate()
                proc.kill()
            else:
                proc.send_signal(signal.SIGINT)
            p = Pout(*proc.communicate())
            print(p)
            out.append(Pout(*proc.communicate()))
        return out

    def is_empty(self) -> bool:
        return not len(self.__proc_list)
