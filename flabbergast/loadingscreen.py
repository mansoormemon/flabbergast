import arcade as arc

from .assets import asset
from .dataproxy import Meta
from .references import SceneList

from .assets import (
    AUDIO_KEYBOARDTYPING,
    LOGO_GAME
)

from . import xarcade as xarc


class LoadingScreen(xarc.AbstractScene):
    TIMEOUT = 3

    MASCOT_CORP_Y_BOTTOM = 0.06
    MASCOT_CORP_X_LEFT = 0.04

    def __init__(self):
        self._time_elapsed = None

        self._sound = None
        self._sound_player = None
        self._logo_game = None

        super().__init__(SceneList.LOADINGSCREEN)

    def setup(self):
        self._sound = arc.load_sound(asset(AUDIO_KEYBOARDTYPING))

        self._logo_game = arc.load_texture(asset(LOGO_GAME))

    def on_update(self, delta_time):
        self._time_elapsed += delta_time
        seconds = int(self._time_elapsed) % 60
        if seconds == self.TIMEOUT:
            self.curtains.set_scene(SceneList.MAINMENU)

    def draw(self):
        self._logo_game.draw_scaled(Meta.hz_screen_center(), Meta.vt_screen_center())

        super().draw()

    def enter_scene(self, previous_scene):
        self._time_elapsed = 0

        self._sound_player = self._sound.play()

    def leave_scene(self, next_scene):
        arc.stop_sound(self._sound_player)
