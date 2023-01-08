from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from . import xarcade as xarc

PROJECT_ROOT: Path = Path(__file__).parent.parent.resolve()
JSON_INDENT_LEVEL: int = 4


class Singleton:
    instance = None

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            return cls.instance


class User(Singleton):
    FILE: str = "user.json"

    class Key(xarc.Reference):
        NAME = 0
        TEAM = 1

    def __init__(self):
        self.name: str = self.get_data(self.Key.NAME)
        self.team: int = self.get_data(self.Key.TEAM, int)

    @classmethod
    def get_file(cls) -> Path:
        return PROJECT_ROOT.joinpath(cls.FILE)

    @classmethod
    def get_data(cls, key: xarc.Reference, rtype=str) -> bool | int | str:
        with open(cls.get_file()) as file:
            data = json.load(file)
            return rtype(data[key.as_key()])

    @classmethod
    def get_name(cls, alphanumeric_only: bool = True) -> str:
        return str().join(filter(lambda c: c.isalnum() or c.isspace(),
                                 cls.instance.name)) if alphanumeric_only else cls.instance.name

    @classmethod
    def set_name(cls, new_name: str):
        cls.instance.name = new_name

    @classmethod
    def get_team(cls) -> int:
        return cls.instance.team

    @classmethod
    def set_team(cls, new_team: int):
        cls.instance.team = new_team

    @classmethod
    def save(cls):
        data: Dict = cls.instance.__dict__
        json_data: str = json.dumps(data, indent=JSON_INDENT_LEVEL)
        with open(cls.get_file(), "w") as file:
            file.write(f"{json_data}\n")
