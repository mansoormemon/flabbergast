from abc import ABC
from enum import Enum

import arcade_curtains as arc_curts


class Reference(Enum):
    MAINMENU = 0
    PLATFORMER = 1
    SETTINGSPANE = 2


class AbstractScene(arc_curts.BaseScene, ABC):
    def __init__(self, reference, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._reference = reference

    def get_reference(self):
        return self._reference

    def get_reference_name(self):
        return self._reference.name.lower()
