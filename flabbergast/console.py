import arcade as arc

from flabbergast.animations import *
from flabbergast.assets import *
from flabbergast.metadata import *
from flabbergast.util import *


class Console(arc.SpriteList):
    class Level:
        SURFACE = 48

    def __init__(self, scene, surface_level=Level.SURFACE, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._scene = scene
        self._surface_level = surface_level
        self._register = {}
        self._active_sprite = None

    def add_notifier_text(self, text):
        text_sprite = arc.create_text_sprite(text,
                                             0, 0,
                                             arc.color.WHITE_SMOKE,
                                             font_name=assets(FONT_TEKTON))
        text_sprite.center_x = Metadata.hz_screen_center()
        text_sprite.center_y = -self._surface_level

        self._register[text] = text_sprite

        self.append(text_sprite)

    def trigger_notification(self, scene, key):
        if self._active_sprite is not None:
            self.reset()

        text_sprite = self._register[key]
        self._active_sprite = text_sprite
        scene.animations.fire(text_sprite,
                              AnimationSequence.peek_from_bottom(text_sprite.center_x, self._surface_level,
                                                                 speed=Speed.FAST,
                                                                 callback_func=(self.reset_active_sprite,)))

    def reset_active_sprite(self):
        self._active_sprite = None

    def reset(self):
        self._scene.animations.kill(self._active_sprite)
        self._active_sprite.center_y = -self._surface_level
        self.reset_active_sprite()
