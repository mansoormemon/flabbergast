from typing import Optional

import arcade as arc
import arcade_curtains as arc_curts


class Window(arc.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.curtains: Optional[arc_curts.Curtains] = None

    def set_curtains(self, curtains: arc_curts.Curtains):
        self.curtains = curtains

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        self.curtains.current_scene.on_mouse_release(x, y, button, modifiers)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.curtains.current_scene.on_mouse_press(x, y, button, modifiers)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        self.curtains.current_scene.on_mouse_scroll(x, y, scroll_x, scroll_y)

    def on_mouse_leave(self, x: int, y: int):
        self.curtains.current_scene.on_mouse_leave(x, y)

    def on_mouse_enter(self, x: int, y: int):
        self.curtains.current_scene.on_mouse_enter(x, y)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.curtains.current_scene.on_mouse_motion(x, y, dx, dy)

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        self.curtains.current_scene.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_key_release(self, symbol: int, modifiers: int):
        self.curtains.current_scene.on_key_release(symbol, modifiers)

    def on_key_press(self, symbol: int, modifiers: int):
        self.curtains.current_scene.on_key_press(symbol, modifiers)

    def on_update(self, delta_time: float):
        self.curtains.current_scene.on_update(delta_time)
