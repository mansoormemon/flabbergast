import arcade as arc

from . import xarcade as xarc
from .references import SceneList

TIMEOUT = 2


class CutScene(xarc.AbstractScene):
    def __init__(self):
        self.timer = None

        super().__init__(SceneList.CUTSCENE)

    def setup(self):
        self.timer = xarc.EventTimer()
        self.timer.register_event((0, TIMEOUT), lambda *_: self.curtains.set_scene(SceneList.PLATFORMER))

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case arc.key.ESCAPE:
                self.curtains.set_scene(SceneList.MAINMENU)

    def on_update(self, delta_time: float):
        self.timer.tick(delta_time)

    def leave_scene(self, previous_scene: xarc.AbstractScene):
        self.timer.reset()
