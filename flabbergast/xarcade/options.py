from typing import List

import arcade as arc

from flabbergast.assets import (
    AUDIO_POSITIVEINTERFACEHOVER,
    WGT_DEFAULT_ARROWDOWN,
    WGT_DEFAULT_ARROWLEFT,
    WGT_DEFAULT_ARROWRIGHT,
    WGT_DEFAULT_ARROWUP,
    WGT_DOWN_ARROWDOWN,
    WGT_DOWN_ARROWLEFT,
    WGT_DOWN_ARROWRIGHT,
    WGT_DOWN_ARROWUP
)
from .abstractscene import AbstractScene
from .reference import Reference
from ..assets import asset


class AbstractOption(arc.Sprite):
    class TextureTypeList(Reference):
        DEFAULT = 0
        DOWN = 1

    class Scale:
        DEFAULT: float = 0.75
        ON_HOVER: float = 0.8

    class Response:
        NOTE: str = AUDIO_POSITIVEINTERFACEHOVER
        VOLUME: float = 0.4

    def __init__(self, *args, scale: float = Scale.DEFAULT, **kwargs):
        super().__init__(*args, scale=scale, **kwargs)

    def hover(self, *_):
        self.scale = self.Scale.ON_HOVER
        note: arc.Sound = arc.Sound(asset(self.Response.NOTE))
        note.play(self.Response.VOLUME)

    def out(self, *_):
        self.scale = self.Scale.DEFAULT

    def down(self, *_):
        self.set_texture(self.TextureTypeList.DOWN.value)

    def up(self, *_):
        self.set_texture(self.TextureTypeList.DEFAULT.value)

    def click(self, context: AbstractScene, *_):
        pass

    def connect(self, context: AbstractScene, *_):
        context.events.hover(self, self.hover)
        context.events.out(self, self.out)
        context.events.down(self, self.down)
        context.events.up(self, self.up)


class TextOption(AbstractOption):
    def __init__(self, text: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text: str = text

        for texture in self.TextureTypeList:
            texture_path: str = asset(f"images/text/{texture.as_key()}/{self.text}.png")
            self.textures.append(arc.load_texture(texture_path))
        self.set_texture(self.TextureTypeList.DEFAULT.value)


class ImageOption(AbstractOption):
    def __init__(self, textures: List, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for texture in textures:
            texture_path: str = asset(texture)
            self.textures.append(arc.load_texture(texture_path))
        self.set_texture(self.TextureTypeList.DEFAULT.value)


class NavigationArrow(ImageOption):
    class Direction(Reference):
        DOWN = 0
        LEFT = 1
        RIGHT = 2
        UP = 3

    class Scale(ImageOption.Scale):
        DEFAULT: float = 0.34
        ON_HOVER: float = 0.36

    class Response(ImageOption.Response):
        VOLUME: float = 0.1

    def __init__(self, direction: Direction, *args, scale: float = Scale.DEFAULT, **kwargs):
        self.direction = direction

        texture_list: List = []
        if direction == self.Direction.DOWN:
                texture_list += [WGT_DEFAULT_ARROWDOWN, WGT_DOWN_ARROWDOWN]
        elif direction == self.Direction.LEFT:
            texture_list += [WGT_DEFAULT_ARROWLEFT, WGT_DOWN_ARROWLEFT]
        elif direction == self.Direction.RIGHT:
            texture_list += [WGT_DEFAULT_ARROWRIGHT, WGT_DOWN_ARROWRIGHT]
        elif direction == self.Direction.UP:
            texture_list += [WGT_DEFAULT_ARROWUP, WGT_DOWN_ARROWUP]

        super().__init__(texture_list, *args, scale=scale, **kwargs)


class TooltipOption(ImageOption):
    class Scale:
        DEFAULT: float = 0.44
        ON_HOVER: float = 0.48

    def __init__(self, *args, scale: float = Scale.DEFAULT, **kwargs):
        super().__init__(*args, scale=scale, **kwargs)
