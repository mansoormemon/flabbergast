from typing import Any, Dict

import arcade_curtains as arc_curts

from . import xarcade as xarc
from .cutscene import CutScene
from .mainmenu import MainMenu
from .platformer import Platformer
from .references import SceneList
from .settingspane import SettingsPane
from .splashscreen import SplashScreen
from .userdata import User

PARAMS: Dict[str, Any] = {
    "title": "Flabbergast",
    "fullscreen": True
}


class Flabbergast(xarc.Window):
    def __init__(self):
        super().__init__(**PARAMS)

        User()

        self.set_curtains(arc_curts.Curtains(self))

        self.curtains.add_scenes({
            SceneList.SPLASHSCREEN: SplashScreen(),
            SceneList.MAINMENU: MainMenu(),
            SceneList.SETTINGSPANE: SettingsPane(),
            SceneList.PLATFORMER: Platformer(),
            SceneList.CUTSCENE: CutScene()
        })

    def setup(self):
        self.curtains.set_scene(SceneList.SPLASHSCREEN)
