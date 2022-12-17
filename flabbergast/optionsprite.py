import arcade as arc


from flabbergast.assets import *
from flabbergast.util import *


class OptionSprite(arc.Sprite):
    class Effects:
        DEFAULT = 0
        PRESSED = 1

        TOKENS = ["down"]

    class Scale:
        DEFAULT = 0.75
        HOVER = 0.8

    V_PADDING = 96
    H_PADDING = 196

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name

        for effect in self.Effects.TOKENS:
            self.textures.append(
                arc.load_texture(assets(f"{TEXT_DIR}/{effect}/{self.name}.png"))
            )

    class Callback:
        @staticmethod
        def hover(entity, *args):
            RESPONSE_NOTE_VOLUME = 0.2

            entity.scale = entity.Scale.HOVER
            response_note = arc.Sound(assets(MUSIC_MOUSE_HOVER_RESPONSE))
            note_player = response_note.play()
            response_note.set_volume(RESPONSE_NOTE_VOLUME, note_player)

        @staticmethod
        def out(entity, *args):
            entity.scale = entity.Scale.DEFAULT

        @staticmethod
        def down(entity, *args):
            entity.set_texture(entity.Effects.PRESSED)

        @staticmethod
        def up(entity, *args):
            entity.set_texture(entity.Effects.DEFAULT)

        @staticmethod
        def trigger_action(scene, entity, *args):
            pass
