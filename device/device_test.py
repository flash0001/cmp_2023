#! /usr/bin/env python3
from device import Device
import json

dev = Device()

while not dev.next().is_finish_state():
    pass

print(json.dumps(dev.buffer))

dev.next()

print(json.dumps(dev.buffer))
