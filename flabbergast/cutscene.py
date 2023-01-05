import arcade as arc

from .references import SceneList

from . import xarcade as xarc


class CutScene(xarc.AbstractScene):
    TIMEOUT = 2

    def __init__(self):
        self._time_elapsed = None

        super().__init__(SceneList.CUTSCENE)

    def setup(self):
        self.events.key_up(arc.key.ESCAPE, lambda *_: self.curtains.set_scene(SceneList.MAINMENU))

    def on_update(self, delta_time):
        self._time_elapsed += delta_time
        seconds = int(self._time_elapsed) % 60
        if seconds == self.TIMEOUT:
            self.curtains.set_scene(SceneList.PLATFORMER)

    def enter_scene(self, previous_scene):
        self._time_elapsed = 0
