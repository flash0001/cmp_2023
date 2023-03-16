#! /usr/bin/env python3
import os
import json
import asyncio
from flask import Flask, request, make_response, jsonify
from core import ProcPool, Result
from models import Race, ValidationError
from subprocess import PIPE, Popen


app = Flask("server")

DEFAULT_CONFIG = {"port": 5555, "debug": True}

pool = ProcPool()

__dir__ = os.path.abspath(os.path.dirname(__file__))

SUB_PROC_PATH = f"{__dir__}/core/device.py"


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
    if pool.is_empty():
        try:
            data = request.json
            print(data)
            race = Race(
                race_type=data.get("race_type"),
                drivers=data.get("drivers")
            )
            for driver_id in race.drivers:
                pool.add(SUB_PROC_PATH, race.race_type, driver_id)
            res = make_response(Result(ok="the race is running"))
        except json.JSONDecodeError:
            raise ClientError("content type error")
        except ValidationError as err:
            res = app.response_class(
                response=json.dumps(Result(error=err)),
                status=400,
                mimetype='application/json'
            )
        except Exception as err:
            res = app.response_class(
                response=json.dumps(Result(error=err)),
                status=500,
                mimetype='application/json'
            )
    else:
        res = app.response_class(
            response=json.dumps(Result(error="the race is already running")),
            status=404,
            mimetype='application/json'
        )
    return res


@app.route("/race/status", methods=["GET"])
def handler_state():
    status = "finished" if pool.is_empty() else "running"
    return jsonify(Result(ok=status))


@ app.route("/race/finish", methods=["GET"])
def handler_unload():
    if not pool.is_empty():
        data = [*map(lambda res: res.stdout, pool.stop())]
        res = jsonify(Result(ok=data))
    else:
        res = app.response_class(
            response=json.dumps(Result(error="the race is already finished")),
            status=404,
            mimetype='application/json'
        )
    return res


if __name__ == "__main__":
    app.run(**read_config())
