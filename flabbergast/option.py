from enum import Enum

import arcade as arc

from flabbergast.assets import *


class Option(arc.Sprite):
    class TextureTypeList(Enum):
        DEFAULT = 0
        DOWN = 1

    class Scale:
        DEFAULT = 0.75
        ON_HOVER = 0.8

    class Volume:
        RESPONSE_NOTE = 0.6

    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._text = text

        for texture in self.TextureTypeList:
            texture_path = self.make_texture_path(texture)
            self.textures.append(arc.load_texture(assets(texture_path)))
        self.set_texture(self.TextureTypeList.DEFAULT.value)

    def get_text(self):
        return self._text

    def make_texture_path(self, texture):
        return f"{DIR_TEXT}/{texture.name.lower()}/{self._text}.{FMT_IMAGE}"

    class Callback:
        @staticmethod
        def hover(entity, *args):
            entity.scale = entity.Scale.ON_HOVER
            note = arc.Sound(assets(AUDIO_MOUSE_HOVER_RESPONSE))
            note_player = note.play()
            note.set_volume(entity.Volume.RESPONSE_NOTE, note_player)

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
