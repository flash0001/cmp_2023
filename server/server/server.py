#! /usr/bin/env python3

import os
import json
from flask import Flask, request, make_response, jsonify
from core import Device
from models import Race, ValidationError

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


@app.route("/race", methods=["POST"])
def receive_race_params():
    try:
        data = request.json
        print(data)
        data = Race(race_type=data.get("race_type"),
                    drivers=data.get("drivers"))
        results = []
        for driver_id in data.drivers:
            device.set(driver_id=driver_id, race_type=data.race_type.value)
            device.run()
            results.append(device.get())
        res = jsonify(results)
    except json.JSONDecodeError:
        raise ClientError("content type error")
    except ValidationError as err:
        res = app.response_class(
            response=json.dumps({"error": str(err)}),
            status=400,
            mimetype='application/json'
        )
    return res


@app.route("/device/state", methods=["GET"])
def handler_state():
    return jsonify({"state": device.state.name})


@app.route("/device/unload", methods=["GET"])
def handler_unload():
    data = device.get()
    device.reset()
    return jsonify(data)


if __name__ == "__main__":
    app.run(**read_config())
