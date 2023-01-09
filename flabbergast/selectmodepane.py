from __future__ import annotations

from typing import Callable, Optional

import arcade as arc

from . import xarcade as xarc
from .assets import (
    AUDIO_QUICKWARNINGNOTIFICATION,
    BACKGROUND_SELECTMODE,
    TEXT_DEFAULT_SELECTMODE
)
from .assets import asset
from .controlspane import ControlsPane
from .references import CutSceneList, SceneList

SETTINGS_LABEL_Y: Callable = lambda: xarc.Meta.screen_height() * 0.8

CONTROL_OPTIONS_Y: Callable = lambda: xarc.Meta.screen_height() * 0.2


class ModeList(xarc.Reference):
    STORY = 0
    ENDLESS = 1


class ModeOption(xarc.AbstractOption):
    WIDTH: int = 480

    class Scale(xarc.AbstractOption.Scale):
        DEFAULT: float = 0.72
        ON_HOVER: float = 0.75

    class Response(xarc.AbstractOption.Response):
        NOTE: str = AUDIO_QUICKWARNINGNOTIFICATION

    def __init__(self, mode: ModeList, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.reference: ModeList = mode

        for texture in self.TextureTypeList:
            texture_path: str = asset(f"images/modes/{texture.as_key()}/{self.reference.as_key()}.png")
            self.textures.append(arc.load_texture(texture_path))
        self.set_texture(self.TextureTypeList.DEFAULT.value)

    def click(self, context: SelectModePane, *_):
        match self.reference:
            case ModeList.STORY:
                context.curtains.set_scene(CutSceneList.OPENING)
            case ModeList.ENDLESS:
                context.curtains.set_scene(SceneList.PLATFORMER)

    def connect(self, context: SelectModePane, *_):
        super().connect(context)
        context.events.click(self, lambda *args: self.click(context, *args))


class SelectModePane(ControlsPane):
    class ControlOptionList(xarc.Reference):
        BACK = 0

    class ControlOption(ControlsPane.ControlOption):
        def click(self, context: SelectModePane, *args):
            selected_option: context.ControlOptionList = context.ControlOptionList[self.text.upper()]
            match selected_option:
                case context.ControlOptionList.BACK:
                    context.curtains.set_scene(SceneList.MAINMENU)

    def __init__(self, *args, **kwargs):
        self.mode_opts: Optional[arc.SpriteList] = None

        super().__init__(SceneList.SELECTMODEPANE, *args, **kwargs)

    def setup(self, *args, **kwargs):
        super().setup(heading=TEXT_DEFAULT_SELECTMODE, background=BACKGROUND_SELECTMODE)

        self.mode_opts = arc.SpriteList(use_spatial_hash=True)

        x_disp_offset: float = (len(ModeList) - 1) * ModeOption.WIDTH * 0.5
        for n, mode in enumerate(ModeList):
            mode_opt: ModeOption = ModeOption(mode,
                                              center_x=(xarc.Meta.hz_screen_center()
                                                        + (n * ModeOption.WIDTH)
                                                        - x_disp_offset),
                                              center_y=xarc.Meta.vt_screen_center())
            mode_opt.connect(self)
            self.mode_opts.append(mode_opt)

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case arc.key.ESCAPE:
                self.curtains.set_scene(SceneList.MAINMENU)
