from enum import Enum

import arcade as arc

from flabbergast.assets import *

from flabbergast import dataproxy
from flabbergast import options


class Reference(Enum):
    FIESTYLION = 0
    LONEWOLF = 1


class MascotRing(options.ImageOption):
    class Scale:
        DEFAULT = 0.42
        ON_HOVER = 0.44

    class Response(options.ImageOption.Response):
        NOTE = AUDIO_POP
        VOLUME = 0.1


class AvatarMascot(arc.SpriteList):
    class Scale(MascotRing.Scale):
        DELTA = 0.04

    class Volume:
        RESPONSE_NOTE = 0.1

    class Step:
        BACK = -1
        FORWARD = 1

    def __init__(self, center_x, center_y, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._current_reference = dataproxy.User.get_team()

        self._avatars = {}
        for mascot in Reference:
            texture_path = f"{DIR_TEAMS}/{mascot.name.lower()}/mascot.{FMT_IMAGE}"
            self._avatars[mascot.name.lower()] = arc.load_texture(assets(texture_path))

        self._ring = MascotRing([TEAM_SHARED_DEFAULT_MASCOTRING, TEAM_SHARED_DOWN_MASCOTRING],
                                center_x=center_x,
                                center_y=center_y,
                                scale=self.Scale.DEFAULT)
        self.append(self._ring)

        self._previous_state = None

    def get_ring(self):
        return self._ring

    def reset_state(self):
        self._previous_state = None

    def revert_if_unsaved(self):
        if self._previous_state:
            self._current_reference = self._previous_state

    def get_current_reference(self):
        return self._current_reference

    def draw(self, *, filter_=None, pixelated=None, blend_function=None):
        self._avatars[self._current_reference].draw_scaled(self._ring.center_x, self._ring.center_y,
                                                           scale=self.Scale.DEFAULT - self.Scale.DELTA)

        super().draw(filter=filter_, pixelated=pixelated, blend_function=blend_function)

    def change_avatar(self, step):
        if not self._previous_state:
            self._previous_state = self._current_reference

        reference_index = (Reference[self._current_reference.upper()].value + step) % len(Reference)
        reference_list = list(Reference)
        self._current_reference = reference_list[reference_index].name.lower()
