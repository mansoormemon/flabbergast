import json
from pathlib import Path

CONFIG_FILE = "config.json"
ASSETS_FOLDER = "assets"


def get_project_root():
    return Path(__file__).parent.parent


def get_config_file():
    return get_project_root().joinpath(CONFIG_FILE)


def get_config(key, type=str):
    with open(get_config_file()) as file:
        cfg = json.load(file)
        return type(cfg[key])


def get_assets_folder():
    return get_project_root().joinpath(ASSETS_FOLDER)


def assets(path):
    return str(get_assets_folder().joinpath(path))
