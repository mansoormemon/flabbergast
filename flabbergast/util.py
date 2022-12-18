import json
from pathlib import Path

CONFIG_FILE = "config.json"
DATA_FILE = "data.json"
ASSETS_FOLDER = "assets"


def get_project_root():
    return Path(__file__).parent.parent


def get_config_file():
    return get_project_root().joinpath(CONFIG_FILE)


def get_config(key, type=str):
    with open(get_config_file()) as file:
        cfg = json.load(file)
        return type(cfg[key])


def get_data_file():
    return get_project_root().joinpath(DATA_FILE)


def get_data(key, type=str):
    with open(get_data_file()) as file:
        data = json.load(file)
        return data[key]


def update_data(key, value):
    with open(get_data_file()) as file:
        data = json.load(file)
        data[key] = value

    INDENT_LEVEL = 4
    json_data = json.dumps(data, indent=INDENT_LEVEL)
    with open(get_data_file(), "w") as file:
        file.write(f"{json_data}\n")


def get_assets_folder():
    return get_project_root().joinpath(ASSETS_FOLDER)


def assets(path):
    return str(get_assets_folder().joinpath(path))
