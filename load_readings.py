import json


def get_readings():
    """Load readings from local filesysystem.
    There's no need to refactor this function.
    The json library reads until EOF and then loads into memory.
    Returns a dictionary."""
    with open('./readings.json', 'r') as f:
        readings = json.load(f)
    return readings
