from . import xarcade as xarc


class MascotList(xarc.Reference):
    FIESTYLION = 0
    LONEWOLF = 1


class SceneList(xarc.Reference):
    SPLASHSCREEN = 0
    MAINMENU = 1
    SETTINGSPANE = 2
    SELECTMODEPANE = 3
    PLATFORMER = 4
    NONE = -1


class CutSceneList(xarc.Reference):
    OPENING = 0
