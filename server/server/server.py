#! /usr/bin/env python3

import os
import json
from flask import Flask, request, make_response, jsonify
from core import Device, RACE_TYPE

device = Device()

app = Flask("server")

DEFAULT_CONFIG = {"port": 5555, "debug": True}


class ClientError(Exception):
    pass


def read_config():
    # TODO make the directory in home
    home_dir = os.path.dirname(__file__)
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


def validate_driver_id(idx):
    if not isinstance(idx, int):
        raise ClientError(f"driver_id must be int, but type is {type(idx)}")
    elif idx < 1 or idx > 99:
        raise ClientError("value of driver_id out of range")


def validate_race_type(race_type):
    if not isinstance(race_type, str):
        raise ClientError(
            f"race_type must be str, but type is {type(race_type)}")
    if race_type not in RACE_TYPE:
        raise ClientError("unknown type of race")


def validate_user_data(data):
    if not isinstance(data, list):
        raise ClientError(f"data must be list, but received {type(data)}")
    for item in data:
        validate_driver_id(item.get("driver_id"))
        validate_race_type(item.get("race_type"))


@app.route("/race", methods=["POST"])
def receive_race_params():
    try:
        data = request.json
        validate_user_data(data)
        device.set_race_state()
        device.next()
        res = jsonify({"message": "race is finished"})
    except json.JSONDecodeError:
        raise ClientError("content type error")
    except ClientError as err:
        res = app.response_class(
            response=json.dumps({"error": str(err)}),
            status=400,
            mimetype='application/json'
        )
    return res


@app.route("/device/state", methods=["GET"])
def handler_state():
    return jsonify({"state": device.state.name})


@app.route("/device/unload", methods=["POST"])
def handler_unload():
    if device.is_finish_state():
        data = device.buffer
        device.reset()
    else:
        data = []
    return jsonify({"buffer": data})


if __name__ == "__main__":
    app.run(**read_config())
