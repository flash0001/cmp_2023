#! /usr/bin/env bash

curl -X POST\
  -H "Content-Type: application/json"\
  --data '[{"driver_id": 1, "race_type": "top_8"}, {"driver_id": 1, "race_type": "top_4"}]'\
  http://127.0.0.1:5555/race



1 99
{"race_type": "top_8", "drivers": [2, 3, 4]}