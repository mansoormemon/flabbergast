from abc import ABC

import arcade_curtains as arc_curts

from .reference import Reference


class AbstractScene(arc_curts.BaseScene, ABC):
    def __init__(self, reference: Reference, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.reference: Reference = reference

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        pass

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        pass

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        pass

    def on_mouse_leave(self, x: int, y: int):
        pass

    def on_mouse_enter(self, x: int, y: int):
        pass

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        pass

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        pass

    def on_key_release(self, symbol: int, modifiers: int):
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        pass

    def on_update(self, delta_time: float):
        pass
