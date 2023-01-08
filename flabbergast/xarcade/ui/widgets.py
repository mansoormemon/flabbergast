from enum import Enum
from typing import Tuple

import arcade as arc
import arcade.gui as arc_gui

from ..options import TooltipOption
from ...assets import (
    ICON_DEFAULT_EDITPENCIL,
    ICON_DOWN_EDITPENCIL,
    WGT_DEFAULT_INPUTBOX,
    WGT_DOWN_INPUTBOX
)
from ...assets import asset

FONT_COLOR: Tuple[int, int, int] = arc.color.WINE_DREGS
FONT_NAME: str = "Tekton Display Ssi"
FONT_SIZE: int = 22

EDIT_BUTTON_X_CENTER_X: float = 0.36

BOX_OFFSET: int = 8

CHAR_LIMIT: int = 13


class InputBox(arc_gui.UIInputText):
    class TextureTypeList(Enum):
        DEFAULT = 0
        DOWN = 1

    class Scale:
        DELTA = 0.08
        DEFAULT = 0.55

    def __init__(self, text, ui_manager, widget_list, center_x, center_y):
        self.ui_manager: arc_gui.UIManager = ui_manager

        self.widget_list: arc.SpriteList = widget_list

        self.background: arc.Sprite = arc.Sprite(center_x=center_x,
                                                 center_y=center_y,
                                                 scale=self.Scale.DEFAULT)
        self.background.textures = [arc.load_texture(asset(WGT_DEFAULT_INPUTBOX)),
                                    arc.load_texture(asset(WGT_DOWN_INPUTBOX))]
        self.background.set_texture(self.TextureTypeList.DEFAULT.value)
        self.widget_list.append(self.background)

        x_offset: float = self.background.width * EDIT_BUTTON_X_CENTER_X
        self.edit_button: TooltipOption = TooltipOption([ICON_DEFAULT_EDITPENCIL, ICON_DOWN_EDITPENCIL],
                                                        center_x=center_x + x_offset,
                                                        center_y=center_y)
        self.widget_list.append(self.edit_button)

        width: float = self.background.width * (self.Scale.DEFAULT + self.Scale.DELTA)
        height: float = self.background.height * (self.Scale.DEFAULT + self.Scale.DELTA)
        x: float = center_x - (width / 2) - BOX_OFFSET
        y: float = center_y - (height / 2) - BOX_OFFSET
        super().__init__(text=text,
                         x=x,
                         y=y,
                         width=width,
                         height=height,
                         text_color=FONT_COLOR,
                         font_name=FONT_NAME,
                         font_size=FONT_SIZE)

        self.previous_active_state = False
        self.previous_text = self.text

        self.previous_state = None

    def connect(self, context):
        self.edit_button.connect(context)
        context.events.click(self.edit_button, self.on_focus)

    def on_update(self, delta_time):
        if self.previous_active_state != self._active:
            if not self._active:
                self.on_blur()
            self.previous_active_state = self._active

        if self.previous_text != self.text:
            self.text = self.text[:CHAR_LIMIT]
            self.previous_text = self.text

    def on_focus(self, *args):
        if not self.previous_state:
            self.previous_state = self.text

        self.ui_manager.enable()
        self._active = True
        self.trigger_full_render()
        self.caret.on_activate()
        self.caret.position = len(self.text)
        self.edit_button.visible = False
        self.background.set_texture(self.TextureTypeList.DOWN.value)

    def on_blur(self, *args):
        self.ui_manager.disable()
        self.edit_button.visible = True
        self.background.set_texture(self.TextureTypeList.DEFAULT.value)

    def flush(self):
        self.previous_state = None

    def stabilize(self):
        if self.previous_state:
            self.text = self.previous_state
            self.trigger_full_render()
