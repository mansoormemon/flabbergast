from abc import ABC
from enum import Enum

import arcade as arc
import json

from flabbergast import mathematics
from flabbergast import util


class SingletonData(ABC):
    instance = None

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            return cls.instance

    @classmethod
    def load(cls):
        cls()

    @classmethod
    def get(cls):
        return cls.instance


class Configuration(SingletonData):
    FILE = "config.json"

    class Key(Enum):
        SCREEN_TITLE = 0
        FULLSCREEN = 1

    def __init__(self):
        self.SCREEN_TITLE = self.get_config(self.Key.SCREEN_TITLE)
        self.FULLSCREEN = self.get_config(self.Key.FULLSCREEN, bool)

    @classmethod
    def get_config_file(cls):
        return util.get_project_root().joinpath(cls.FILE)

    @classmethod
    def get_config(cls, key, rtype=str):
        if isinstance(key, Enum):
            key = key.name.lower()

        with open(cls.get_config_file()) as file:
            cfg = json.load(file)
            return rtype(cfg[key])

    @classmethod
    def screen_title(cls):
        return cls.instance.SCREEN_TITLE

    @classmethod
    def fullscreen(cls):
        return cls.instance.FULLSCREEN


class Meta(SingletonData):
    def __init__(self):
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = arc.get_window().get_size()

    @classmethod
    def screen_width(cls):
        return cls.instance.SCREEN_WIDTH

    @classmethod
    def screen_height(cls):
        return cls.instance.SCREEN_HEIGHT

    @classmethod
    def screen_size(cls):
        return cls.screen_width(), cls.screen_height()

    @classmethod
    def hz_screen_center(cls):
        return mathematics.half(cls.screen_width())

    @classmethod
    def vt_screen_center(cls):
        return mathematics.half(cls.screen_height())

    @classmethod
    def screen_center(cls):
        return cls.hz_screen_center(), cls.vt_screen_center()


class User(SingletonData):
    FILE = "userdata.json"

    class Key(Enum):
        NAME = 0
        TEAM = 1

    def __init__(self):
        self.name = self.get_data(self.Key.NAME)
        self.team = self.get_data(self.Key.TEAM)

    @classmethod
    def get_file(cls):
        return util.get_project_root().joinpath(cls.FILE)

    @classmethod
    def get_data(cls, key, rtype=str):
        if isinstance(key, Enum):
            key = key.name.lower()

        with open(cls.get_file()) as file:
            data = json.load(file)
            return rtype(data[key])

    @classmethod
    def get_name(cls, alphanumeric_only=True):
        return str().join(
            filter(lambda c: c.isalnum() or c.isspace(), cls.instance.name)
        ) if alphanumeric_only else cls.instance.name

    @classmethod
    def set_name(cls, new_name):
        cls.instance.name = new_name

    @classmethod
    def get_team(cls):
        return cls.instance.team

    @classmethod
    def set_team(cls, new_team):
        if isinstance(new_team, Enum):
            new_team = new_team.name.lower()
        cls.instance.team = new_team

    @classmethod
    def save(cls):
        JSON_INDENT_LEVEL = 4

        data = cls.instance.__dict__
        json_data = json.dumps(data, indent=JSON_INDENT_LEVEL)
        with open(cls.get_file(), "w") as file:
            file.write(f"{json_data}\n")
