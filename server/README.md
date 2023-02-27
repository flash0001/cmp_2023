# Race

/race POST

mime: application/json

```json
{
  "type": "array",
  "item": {
    "type": "object",
    "items": {
      "driver_id": {
        "type": "number",
        "min": 1,
        "max": 99
      },
      "race_type": {
        "type": "string",
        "enum": [
          "qualifying",
          "top_32",
          "top_16",
          "top_8",
          "semifinal",
          "battle for 3rd place",
          "final"
        ]
      }
    }
  }
}
```

```json
[{ "driver_id": 1, "race_type": "final" }]
```

# Device

/device/state GET

/device/unload POST
