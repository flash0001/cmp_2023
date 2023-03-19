import os
import time
import json

__dir__ = os.path.abspath(os.path.dirname(__file__))


class Archiver:
    PATH = os.path.join(__dir__, "..", "..", "archives")

    def make(self, data):
        if not os.path.isdir(Archiver.PATH):
            os.mkdir(Archiver.PATH)
        t = str(int(time.time()))
        path = os.path.join(Archiver.PATH, f"arch_{t}.json")
        with open(path, "w") as fp:
            json.dump(data, fp, ensure_ascii=False, indent=2)
        return path


arc = Archiver()
