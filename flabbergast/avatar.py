import arcade as arc

from .assets import asset
from .dataproxy import AtomicData, Meta, User
from .xarcade.options import ImageOption
from .references import MascotList

from .assets import (
    AUDIO_POP,
    TEAM_SHARED_DEFAULT_MASCOTRING,
    TEAM_SHARED_DOWN_MASCOTRING
)


class _Ring(ImageOption):
    class Scale(ImageOption.Scale):
        DEFAULT = 0.42
        ON_HOVER = 0.44

    class Response(ImageOption.Response):
        NOTE = AUDIO_POP
        VOLUME = 0.1


class Avatar(arc.SpriteList):
    class Scale(_Ring.Scale):
        DELTA = 0.04

    class Step:
        BACK = -1
        FORWARD = 1

    def __init__(self, center_x, center_y, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.team = AtomicData(User.get_team())

        self._avatars = {}
        for mascot in MascotList:
            texture_path = asset(f"teams/{mascot.name.lower()}/mascot.png")
            self._avatars[mascot.name.lower()] = arc.load_texture(texture_path)

        self._ring = _Ring([TEAM_SHARED_DEFAULT_MASCOTRING, TEAM_SHARED_DOWN_MASCOTRING],
                           center_x=center_x,
                           center_y=center_y,
                           scale=self.Scale.DEFAULT)
        self.append(self._ring)

    def get_ring(self):
        return self._ring

    def draw(self, *args, filter_=None, pixelated=None, blend_function=None):
        self._avatars[self.team.data].draw_scaled(self._ring.center_x,
                                                  self._ring.center_y,
                                                  self.Scale.DEFAULT - self.Scale.DELTA)

        super().draw(filter=filter_, pixelated=pixelated, blend_function=blend_function)

    def change_avatar(self, step):
        reference_list = list(MascotList)
        reference_index = (MascotList[self.team.data.upper()].value + step) % len(reference_list)
        self.team.data = reference_list[reference_index].name.lower()
