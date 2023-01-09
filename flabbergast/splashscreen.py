from typing import Optional, Tuple

import arcade as arc

from . import xarcade as xarc
from .assets import (
    AUDIO_KEYBOARDTYPING,
    LOGO_GAME
)
from .assets import asset
from .references import SceneList

TIME_SPAN: Tuple[int, int] = (0, 4)

FONT_COLOR: Tuple[int, int, int] = arc.color.WHITE_SMOKE
FONT_NAME: str = "Tekton Display Ssi"
FONT_SIZE: int = 8

TAG_COPYRIGHT: str = "© NightStalker Corp. 2023"
TAG_COPYRIGHT_Y: int = 64


class SplashScreen(xarc.AbstractScene):
    def __init__(self, *args, **kwargs):
        self.timer: Optional[xarc.EventTimer] = None
        self.sound: Optional[arc.Sound] = None
        self.sound_player: Optional[arc.sound.media.Player] = None
        self.logo_game: Optional[arc.Texture] = None
        self.tag_copyright: Optional[arc.Text] = None

        super().__init__(SceneList.SPLASHSCREEN, *args, **kwargs)

    def setup(self, *args, **kwargs):
        self.timer = xarc.EventTimer()
        self.timer.register_event(TIME_SPAN, lambda: self.curtains.set_scene(SceneList.MAINMENU))

        self.sound = arc.load_sound(asset(AUDIO_KEYBOARDTYPING))

        self.logo_game = arc.load_texture(asset(LOGO_GAME))

        self.tag_copyright = arc.Text(TAG_COPYRIGHT,
                                      start_x=xarc.Meta.hz_screen_center(),
                                      start_y=TAG_COPYRIGHT_Y,
                                      color=FONT_COLOR,
                                      font_name=FONT_NAME,
                                      font_size=FONT_SIZE,
                                      anchor_x="center", anchor_y="center")

    def enter_scene(self, previous_scene: xarc.AbstractScene):
        self.sound_player = self.sound.play()

    def leave_scene(self, next_scene: xarc.AbstractScene):
        arc.stop_sound(self.sound_player)
        self.timer.reset()

    def draw(self):
        self.logo_game.draw_scaled(xarc.Meta.hz_screen_center(), xarc.Meta.vt_screen_center())
        self.tag_copyright.draw()

        super().draw()

    def on_update(self, delta_time: float):
        self.timer.tick(delta_time)
