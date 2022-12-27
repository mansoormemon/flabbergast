from enum import Enum

import arcade as arc

from flabbergast.assets import *


class Reference(Enum):
    FIESTYLION = 0
    LONEWOLF = 1


class AvatarMascot(arc.SpriteList):
    IMAGE_FILE_NAME = "mascotring"

    class TextureTypeList(Enum):
        DEFAULT = 0
        DOWN = 1

    class Scale:
        DELTA = 0.02
        DEFAULT = 0.44
        ON_HOVER = 0.448

    class Volume:
        RESPONSE_NOTE = 0.1

    def __init__(self, reference, center_x, center_y, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._reference = reference

        self._avatar_texture = arc.load_texture(assets(self.get_mascot_path()))

        self._ring = arc.Sprite(scale=self.Scale.DEFAULT, center_x=center_x, center_y=center_y)
        for texture in self.TextureTypeList:
            texture_path = self.make_texture_path(texture)
            self._ring.textures.append(arc.load_texture(assets(texture_path)))
        self._ring.set_texture(self.TextureTypeList.DEFAULT.value)
        self.append(self._ring)

    def get_reference(self):
        return self._reference

    def get_reference_name(self):
        return self._reference.name.lower()

    def get_ring(self):
        return self._ring

    def make_texture_path(self, texture):
        return f"{DIR_TEAMS}/shared/{texture.name.lower()}/{self.IMAGE_FILE_NAME}.{FMT_IMAGE}"

    def get_mascot_path(self):
        match self._reference:
            case Reference.FIESTYLION:
                return TEAM_FIESTYLION_MASCOT
            case Reference.LONEWOLF:
                return TEAM_LONEWOLF_MASCOT

    def draw(self, *, filter_=None, pixelated=None, blend_function=None):
        self._avatar_texture.draw_scaled(self._ring.center_x, self._ring.center_y,
                                         scale=self.Scale.DEFAULT - self.Scale.DELTA)

        super().draw(filter=filter_, pixelated=pixelated, blend_function=blend_function)

    class Callback:
        @staticmethod
        def hover(entity, *args):
            sprite_list, *residue = entity.sprite_lists
            entity.scale = sprite_list.Scale.ON_HOVER
            note = arc.Sound(assets(AUDIO_LONGPOP))
            note_player = note.play()
            note.set_volume(sprite_list.Volume.RESPONSE_NOTE, note_player)

        @staticmethod
        def out(entity, *args):
            sprite_list, *residue = entity.sprite_lists
            entity.scale = sprite_list.Scale.DEFAULT

        @staticmethod
        def down(entity, *args):
            sprite_list, *residue = entity.sprite_lists
            entity.set_texture(sprite_list.TextureTypeList.DOWN.value)

        @staticmethod
        def up(entity, *args):
            sprite_list, *residue = entity.sprite_lists
            entity.set_texture(sprite_list.TextureTypeList.DEFAULT.value)

        @staticmethod
        def trigger_click_action(context, entity, *args):
            pass
