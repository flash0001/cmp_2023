# Race

/race POST

mime: application/json

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
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
[
  { "driver_id": 1, "race_type": "final" },
  { "driver_id": 3, "race_type": "final" }
]
```

```json
{
  "type": "object",
  "properties": {
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
    },
    "drivers": {
      "type": "array",
      "items": {
        "type": "number",
        "min": 1,
        "max": 99
      }
    }
  }
}
```

```json
{ "race_type": "top_4", "drivers": [1, 10] }
```

# Device

/device/state GET

/device/unload POST
