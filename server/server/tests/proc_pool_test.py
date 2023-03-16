#! /usr/bin/env python3
import os
if __name__ == "__main__":
    import sys
    __dir__ = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(f"{__dir__}/..")

from core import ProcPool, Pout
import time

path = f"{os.path.dirname(__file__)}/../core/device.py"

pool = ProcPool()
pool.add("python3", path, 1, "final")
pool.add("python3", path, 3, "final")
pool.add("python3", path, 4, "final")

duration = 2
print(f"waiting for the end of sleep({duration})...")
time.sleep(duration)
print("complete!")
for out in pool.stop():
    print(out)
    print("-"*20)
