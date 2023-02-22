#! /usr/bin/env python3
from flask import Flask, request, make_response, jsonify
from core import Device
from json import JSONDecodeError
from functools import reduce

device = Device()

app = Flask("server")
print(__file__)

RACE_TYPE = [
    "qualifying", "top_32", "top_16",
    "top_8", "semifinal", "battle for 3rd place", "final",
]


class ClientError(Exception):
    pass


def read_config():
    return {"port": 5555, "debug": True}


def validate_driver_id(idx):
    if not isinstance(idx, int):
        raise ClientError(f"driver_id must be int, but type is {type(idx)}")
    elif idx < 1 or idx > 99:
        raise ClientError("value of driver_id out of range")


def validate_race_type(race_type):
    if isinstance(race_type, str):
        raise ClientError(
            f"race_type must be str, but type is {type(race_type)}")
    if race_type not in RACE_TYPE:
        raise ClientError("unknown type of race")


def validate_user_data(data):
    if not isinstance(data, dict):
        raise ClientError(f"data must be tuple, but received {type(data)}")
    validate_driver_id(data.get("driver_id"))
    validate_race_type(data.get("race_type"))


@app.route("/", methods=["POST"])
def receive_race_params():
    try:
        data = request.json
        validate_user_data(data)
    except JSONDecodeError:
        raise ClientError("content type error")
    except ClientError as err:
        res = app.response_class(
            response=json.dumps({"error": str(err)}),
            status=400,
            mimetype='application/json'
        )
    return res


@app.route("/state", methods=["GET"])
def handler_state():
    return jsonify({"state": device.state.nam})


if __name__ == "__main__":
    app.run(**read_config())
