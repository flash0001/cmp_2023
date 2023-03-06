import os
import requests
import json


DEFAULT_CONFIG = {"port": 5555, "debug": True}


def read_config():
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
URL = f"http://localhost:{cfg['port']}"
resp = requests.post(
    f"{URL}/race",
    json={"race_type": "final", "drivers": [1]}
)

if resp.ok:
    print(resp.json())
else:
    print(resp.text)
