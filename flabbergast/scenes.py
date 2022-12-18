from abc import ABC
from enum import Enum

import arcade_curtains as arc_curts


class Scene(Enum):
    MAIN_MENU = 0
    LEVEL = 1
    SETTINGS = 2


class NamedScene(arc_curts.BaseScene, ABC):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._name = name

    def get_name(self):
        return self._name
