import json

from pathlib import Path


def get_path():
    cwd = Path(__file__).parents[1]
    cwd = str(cwd)
    return cwd


def read_json():
    cwd = get_path()
    with open(cwd + "/settings/guilds.json", "r") as file:
        data = json.load(file)
    return data


def write_json(data):
    cwd = get_path()
    with open(cwd + "/settings/guilds.json", "w") as file:
        json.dump(data, file, indent=4)