from __future__ import annotations

from enum import Enum
from typing import Callable, Optional

import arcade as arc

from . import xarcade as xarc
from .assets import (
    BACKGROUND_PANE
)
from .assets import asset
from .references import SceneList

HEADING_Y: Callable = lambda: xarc.Meta.screen_height() * 0.8

CONTROL_OPTIONS_Y: Callable = lambda: xarc.Meta.screen_height() * 0.2


class ControlsPane(xarc.AbstractScene):
    class ControlOptionList(Enum):
        pass

    class ControlOption(xarc.TextOption):
        WIDTH: int = 384

        class Scale(xarc.TextOption.Scale):
            DEFAULT: float = 0.6
            ON_HOVER: float = 0.65

        class Response(xarc.TextOption.Response):
            VOLUME: float = 0.3

        def __init__(self, text: str, *args, scale: float = Scale.DEFAULT, **kwargs):
            super().__init__(text, *args, scale=scale, **kwargs)

        def connect(self, context: ControlsPane, *_):
            super().connect(context)
            context.events.click(self, lambda *args: self.click(context, *args))

    def __init__(self, reference: SceneList, *args, **kwargs):
        self.background: Optional[arc.Texture] = None
        self.pane: Optional[arc.Texture] = None
        self.interactive_elements: Optional[arc.SpriteList] = None
        self.heading: Optional[arc.Sprite] = None
        self.control_opts: Optional[arc.SpriteList] = None

        super().__init__(reference, *args, **kwargs)

    def setup(self, *args, **kwargs):
        self.background = arc.load_texture(asset(kwargs["background"]))

        self.pane = arc.load_texture(asset(BACKGROUND_PANE))

        self.interactive_elements = arc.SpriteList(use_spatial_hash=True)

        self.heading = arc.Sprite(asset(kwargs["heading"]), center_x=xarc.Meta.hz_screen_center(), center_y=HEADING_Y())
        self.events.hover(self.heading,
                          lambda entity, *_: self.animations.fire(entity,
                                                                  xarc.Animation.inflate(entity.scale)))
        self.events.out(self.heading,
                        lambda entity, *_: self.animations.fire(entity,
                                                                xarc.Animation.deflate(entity.scale)))
        self.interactive_elements.append(self.heading)
        self.control_opts = arc.SpriteList(use_spatial_hash=True)
        x_disp_offset: float = (len(self.ControlOptionList) - 1) * self.ControlOption.WIDTH * 0.5
        for n, opt in enumerate(self.ControlOptionList):
            ctrl_opt: self.ControlOption = self.ControlOption(opt.as_key(),
                                                              center_x=(xarc.Meta.hz_screen_center()
                                                                        + (n * self.ControlOption.WIDTH)
                                                                        - x_disp_offset),
                                                              center_y=CONTROL_OPTIONS_Y())
            ctrl_opt.connect(self)
            self.control_opts.append(ctrl_opt)

    def draw(self):
        self.background.draw_scaled(xarc.Meta.hz_screen_center(), xarc.Meta.vt_screen_center())
        self.pane.draw_scaled(xarc.Meta.hz_screen_center(), xarc.Meta.vt_screen_center())

        super().draw()
