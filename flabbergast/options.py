from enum import Enum

import arcade as arc

from flabbergast.assets import *


class AbstractOption(arc.Sprite):
    class TextureTypeList(Enum):
        DEFAULT = 0
        DOWN = 1

    class Scale:
        DEFAULT = 0.75
        ON_HOVER = 0.8

    class Response:
        NOTE = AUDIO_MOUSE_HOVER_RESPONSE
        VOLUME = 0.4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Callback:
        @staticmethod
        def hover(entity, *args):
            entity.scale = entity.Scale.ON_HOVER
            note = arc.Sound(assets(entity.Response.NOTE))
            note_player = note.play()
            note.set_volume(entity.Response.VOLUME, note_player)

        @staticmethod
        def out(entity, *args):
            entity.scale = entity.Scale.DEFAULT

        @staticmethod
        def down(entity, *args):
            entity.set_texture(entity.TextureTypeList.DOWN.value)

        @staticmethod
        def up(entity, *args):
            entity.set_texture(entity.TextureTypeList.DEFAULT.value)

        @staticmethod
        def trigger_click_action(context, entity, *args):
            pass


class TextOption(AbstractOption):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._text = text

        for texture in self.TextureTypeList:
            texture_path = f"{DIR_TEXT}/{texture.name.lower()}/{self._text}.{FMT_IMAGE}"
            self.textures.append(arc.load_texture(assets(texture_path)))
        self.set_texture(self.TextureTypeList.DEFAULT.value)

    def get_text(self):
        return self._text


class ImageOption(AbstractOption):
    def __init__(self, textures, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for texture in textures:
            self.textures.append(arc.load_texture(assets(texture)))

        self.set_texture(self.TextureTypeList.DEFAULT.value)


class NavigationArrow(ImageOption):
    class Direction(Enum):
        DOWN = 0
        LEFT = 1
        RIGHT = 2
        UP = 3

    class Scale(ImageOption.Scale):
        DEFAULT = 0.34
        ON_HOVER = 0.36

    class Response(ImageOption.Response):
        VOLUME = 0.1

    def __init__(self, direction, *args, **kwargs):
        texture_list = None
        match direction:
            case self.Direction.DOWN:
                texture_list = [WGT_DEFAULT_ARROWDOWN, WGT_DOWN_ARROWDOWN]
            case self.Direction.LEFT:
                texture_list = [WGT_DEFAULT_ARROWLEFT, WGT_DOWN_ARROWLEFT]
            case self.Direction.RIGHT:
                texture_list = [WGT_DEFAULT_ARROWRIGHT, WGT_DOWN_ARROWRIGHT]
            case self.Direction.UP:
                texture_list = [WGT_DEFAULT_ARROWUP, WGT_DOWN_ARROWUP]

        super().__init__(texture_list, *args, scale=self.Scale.DEFAULT, **kwargs)
