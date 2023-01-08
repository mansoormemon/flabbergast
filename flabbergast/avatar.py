from __future__ import annotations

import arcade as arc

from . import xarcade as xarc
from .assets import (
    AUDIO_POP,
    TEAM_SHARED_DEFAULT_MASCOTRING,
    TEAM_SHARED_DOWN_MASCOTRING
)
from .assets import asset
from .references import MascotList
from .userdata import User


class _Ring(xarc.ImageOption):
    class Scale(xarc.ImageOption.Scale):
        DEFAULT: float = 0.42
        ON_HOVER: float = 0.43

    class Response(xarc.ImageOption.Response):
        NOTE: str = AUDIO_POP
        VOLUME: float = 0.1

    def __init__(self, *args, scale: float = Scale.DEFAULT, **kwargs):
        super().__init__(*args, scale=scale, **kwargs)


class _AvatarNavigationArrow(xarc.NavigationArrow):
    def click(self, context: xarc.AbstractScene, *args):
        parent, *_ = args
        match self.direction:
            case self.Direction.LEFT:
                parent.change_mascot(parent.Step.BACK)
            case self.Direction.RIGHT:
                parent.change_mascot(parent.Step.FORWARD)

    def connect(self, context: xarc.AbstractScene, *args):
        super().connect(context)
        parent, *_ = args
        context.events.click(self, lambda *args_: self.click(context, parent, *args_))


class C:
    ARROW_LEFT_X: float = lambda: xarc.Meta.screen_width() * 0.35
    ARROW_RIGHT_X: float = lambda: xarc.Meta.screen_width() * 0.65


class Avatar(arc.SpriteList):
    class Scale(_Ring.Scale):
        DELTA: float = 0.04

    class Step:
        BACK: int = -1
        FORWARD: int = 1

    def __init__(self, center_x, center_y, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.team: xarc.AtomicData = xarc.AtomicData(User.get_team())

        self.mascots: list = []
        for mascot in MascotList:
            texture_path: str = asset(f"images/teams/{mascot.as_key()}/mascot.png")
            self.mascots.append(arc.load_texture(texture_path))

        self.ring: _Ring = _Ring([TEAM_SHARED_DEFAULT_MASCOTRING, TEAM_SHARED_DOWN_MASCOTRING],
                                 center_x=center_x,
                                 center_y=center_y)
        self.append(self.ring)

        self.avatar_arrow_left = _AvatarNavigationArrow(xarc.NavigationArrow.Direction.LEFT,
                                                        center_x=C.ARROW_LEFT_X(),
                                                        center_y=center_y)
        self.append(self.avatar_arrow_left)

        self.avatar_arrow_right = _AvatarNavigationArrow(xarc.NavigationArrow.Direction.RIGHT,
                                                         center_x=C.ARROW_RIGHT_X(),
                                                         center_y=center_y)
        self.append(self.avatar_arrow_right)

    def draw(self, *args, filter_=None, pixelated=None, blend_function=None):
        self.mascots[self.team.data].draw_scaled(self.ring.center_x, self.ring.center_y,
                                                 self.Scale.DEFAULT - self.Scale.DELTA)

        super().draw(filter=filter_, pixelated=pixelated, blend_function=blend_function)

    def change_mascot(self, step: int):
        self.team.data = (self.team.data + step) % len(MascotList)

    def connect(self, context: xarc.AbstractScene):
        self.ring.connect(context)
        self.avatar_arrow_left.connect(context, self)
        self.avatar_arrow_right.connect(context, self)

    def flush(self):
        self.team.flush()

    def stabilize(self):
        self.team.stabilize()
