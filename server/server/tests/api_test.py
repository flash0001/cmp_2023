#! /usr/bin/env python3
import os
if __name__ == "__main__":
    import sys
    __dir__ = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(f"{__dir__}/..")

from core import Result
from requests import Response
import requests
import json
import time


DEFAULT_CONFIG = {"port": 5555, "debug": True}


def read_config() -> dict[str, str | int]:
    # TODO make the directory in home
    home_dir = os.path.dirname(__file__) + "/.."
    cfg_file = os.path.join(home_dir, "config.json")
    cfg = {**DEFAULT_CONFIG}
    try:
        with open(cfg_file) as fl:
            data = json.load(fl)
        cfg["port"] = data.get("port", DEFAULT_CONFIG["port"])
        cfg["debug"] = data.get("debug", DEFAULT_CONFIG["debug"])
    except (FileNotFoundError, json.JSONDecodeError):
        with open(cfg_file, "w") as fp:
            json.dump(DEFAULT_CONFIG, fp)
    return cfg


cfg = read_config()


class HTTPClient:
    PORT = cfg["port"]
    BASE_URL = f"http://127.0.0.1:{PORT}"

    def __init__(self, baseURL: str | None = None):
        self.baseURL = HTTPClient.BASE_URL if baseURL is None else baseURL

    def start_race(self, *, race_type: str, drivers: list[int]):
        res = requests.post(
            f"{self.baseURL}/race",
            json={"race_type": race_type, "drivers": drivers}
        )
        return self.__make_response(res)

    def stop_race(self):
        return self.__make_response(
            requests.get(f"{self.baseURL}/race/finish")
        )

    def get_race_status(self):
        return self.__make_response(
            requests.get(f"{self.baseURL}/race/status")
        )

    def __make_response(self, res: Response) -> Result:
        return Result.translate(res)


if __name__ == "__main__":
    http = HTTPClient()
    res = http.start_race(race_type="final", drivers=[2, 3])
    print(res)
    print(http.get_race_status())
    time.sleep(20)
    res = http.stop_race()
    print(res)
    print(http.get_race_status())
