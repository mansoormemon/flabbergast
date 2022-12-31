import arcade as arc

from flabbergast.assets import asset

from flabbergast.assets import (
    FONT_TEKTON
)

from .. import xarcade as xarc
from ..dataproxy import Meta


class MessageConsole(arc.SpriteList):
    class Level:
        SURFACE = 48

    class Font:
        COLOR = arc.color.WHITE_SMOKE
        PATH = asset(FONT_TEKTON)
        SIZE = 20

    def __init__(self, scene, surface_level=Level.SURFACE, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._scene = scene
        self._surface_level = surface_level
        self._register = {}
        self._active_notification = None

    def add_notifier_text(self, text):
        text_sprite = arc.create_text_sprite(text,
                                             Meta.hz_screen_center(),
                                             -self._surface_level,
                                             self.Font.COLOR,
                                             font_name=self.Font.PATH, font_size=self.Font.SIZE,
                                             anchor_x="center", anchor_y="center")
        self.append(text_sprite)

        self._register[text] = text_sprite

    def reset_active_notification(self):
        self._active_notification = None

    def is_notification_active(self):
        return self._active_notification is not None

    def trigger_notification(self, scene, key):
        if self.is_notification_active():
            self.reset()

        text_sprite = self._register[key]
        self._active_notification = text_sprite
        scene.animations.fire(text_sprite,
                              xarc.Animation.peek_from_bottom(text_sprite.center_x, self._surface_level,
                                                              speed=xarc.Speed.FAST,
                                                              callback=(self.reset_active_notification,)))

    def reset(self):
        if self.is_notification_active():
            self._scene.animations.kill(self._active_notification)
            self._active_notification.center_y = -self._surface_level
            self.reset_active_notification()
