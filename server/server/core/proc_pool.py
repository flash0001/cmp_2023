from subprocess import Popen, PIPE
import signal
import sys


class Pout(dict):
    def __init__(self, stdout: bytes, stderr: bytes):
        super().__init__()
        self["stdout"] = stdout.decode()
        self["stderr"] = stderr.decode()

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


class ProcPool:

    def __init__(self):
        self.__proc_list = []

    def add(self, cmd: str, *args):
        proc = Popen([sys.executable, cmd, *map(lambda x: str(x), args)], stdout=PIPE, stderr=PIPE)
        self.__proc_list.append(proc)

    def stop(self) -> list[Pout]:
        out = []
        while len(self.__proc_list):
            proc = self.__proc_list.pop()
            proc.send_signal(signal.SIGINT)
            out.append(Pout(*proc.communicate()))
        return out

    def is_empty(self) -> bool:
        return not len(self.__proc_list)
