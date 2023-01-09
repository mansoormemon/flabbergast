from typing import Any, Callable, Dict, Iterable, Optional, Tuple

import arcade as arc

from .abstractscene import AbstractScene
from .eventtimer import EventTimer
from .metadata import Meta
from .reference import Reference

FONT_COLOR: Tuple[int, int, int] = arc.color.WHITE_SMOKE
FONT_NAME: str = "Tekton Display Ssi"
FONT_SIZE: int = 12
DELTA_Y: Callable = lambda level: level / 30
ANIMATION_TIMESTAMPS = [(0, 0), (0, 2), (0, 3)]


def _make_animation(timer: EventTimer, timestamps: Iterable[Tuple[int, int]], funcs: Iterable[Callable]):
    for timestamp, func in zip(timestamps, funcs):
        timer.register_event(timestamp, func, False)


class MessageConsole(arc.SpriteList):
    class Level:
        Y: int = 36

    def __init__(self, context: AbstractScene, y_level: float = Level.Y, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.context: AbstractScene = context
        self.y_level: float = y_level
        self.register: Dict[Reference, arc.Text] = {}
        self.active_notification: Optional[arc.Text] = None
        self.timer: EventTimer = EventTimer()
        _make_animation(self.timer, ANIMATION_TIMESTAMPS, [self.notification_slide_up,
                                                           self.notification_slide_down,
                                                           self.reset])

    def add(self, key: Reference, text: str):
        self.register[key] = arc.Text(text,
                                      Meta.hz_screen_center(),
                                      -self.y_level,
                                      color=FONT_COLOR,
                                      font_name=FONT_NAME,
                                      font_size=FONT_SIZE,
                                      anchor_x="center", anchor_y="center")

    def notification_slide_up(self):
        self.active_notification.y += DELTA_Y(self.y_level)

    def notification_slide_down(self):
        self.active_notification.y -= DELTA_Y(self.y_level)

    def on_update(self, delta_time: float = 1 / 60):
        if self.active_notification is not None:
            self.timer.tick(delta_time)

    def trigger_notification(self, key: Reference):
        if self.active_notification is not None:
            self.reset()

        self.active_notification = self.register[key]

    def reset(self):
        if self.active_notification is not None:
            self.active_notification.y = -self.y_level
            self.active_notification = None
            self.timer.reset()

    def draw(self, *, filter_: Any = None, pixelated: Any = None, blend_function: Any = None):
        if self.active_notification is not None:
            self.active_notification.draw()

        super().draw(filter=filter_, pixelated=pixelated, blend_function=blend_function)
