import os
import json
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError

__dir__ = Path(os.path.abspath(os.path.dirname(__file__))) / ".."

class APIServerConfig(BaseModel):
    port: int

class ServerConfig(BaseModel):
    port: int
    debug: bool = False

class Config(BaseModel):
    dark: bool = False
    server: ServerConfig
    api_server: APIServerConfig

with open(__dir__ / "../config.json") as fp:
    data = json.load(fp)

print(data)

config = Config(**data)
