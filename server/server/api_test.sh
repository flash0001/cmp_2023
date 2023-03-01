#! /usr/bin/env bash

curl -X POST\
  -H "Content-Type: application/json"\
  --data '[{"driver_id": 1, "race_type": "top_8"}]'\
  http://127.0.0.1:5555/race

curl -X 