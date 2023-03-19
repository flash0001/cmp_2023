import requests
from requests import Response
from .result import Result
from .config import config


class HTTPClient:
    PORT = config.api_server.port
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
