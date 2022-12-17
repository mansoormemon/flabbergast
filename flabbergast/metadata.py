import arcade as arc

from flabbergast.arithmetic import *


class Metadata:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = arc.get_window().get_size()

    @classmethod
    def load(cls):
        cls()

    @classmethod
    def get(cls):
        return cls.instance

    @classmethod
    def screen_width(cls):
        return cls.instance.SCREEN_WIDTH

    @classmethod
    def screen_height(cls):
        return cls.instance.SCREEN_HEIGHT

    @classmethod
    def screen_size(cls):
        return cls.screen_width(), cls.screen_height()

    @classmethod
    def hz_screen_center(cls):
        return center(cls.screen_width())

    @classmethod
    def vt_screen_center(cls):
        return center(cls.screen_height())

    @classmethod
    def screen_center(cls):
        return cls.hz_screen_center(), cls.vt_screen_center()
