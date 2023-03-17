import json
from requests import Response


class Result(dict):
    def __init__(self, *, ok: str | None = None, error: str | Exception | None = None):
        self["ok"] = ok
        self["error"] = error if error is None else str(error)

    @property
    def ok(self) -> str:
        return self["ok"]

    @property
    def error(self) -> str:
        return self["error"]

    def __str__(self) -> str:
        return json.dumps(self)

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def translate(res: Response) -> 'Result':
        data = res.json()
        if isinstance(data, dict):
            result = Result(
                ok=data.get("ok"),
                error=data.get("error"),
            )
        else:
            if res.ok:
                result = Result(ok=data)
            else:
                result = Result(error=data)
        return result