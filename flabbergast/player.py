from enum import Enum

import arcade as arc

from . import xarcade as xarc


class Player(arc.SpriteCircle):
    class TextureTypeList(Enum):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(5, arc.color.BLUE, *args, **kwargs)

        self.center_x = xarc.Meta.hz_screen_center()
        self.center_y = xarc.Meta.vt_screen_center()

    def start_moving(self, *args):
        pass

    def stop_moving(self, *args):
        pass

    def move_up(self, *args):
        print("up")
        self.center_y += 10

    def move_down(self, *args):
        print("down")
        self.center_y -= 10

    def move_left(self, *args):
        print("left")
        self.center_x -= 10

    def move_right(self, *args):
        print("right")
        self.center_x += 10
