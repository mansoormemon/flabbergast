from enum import Enum

import arcade as arc
import arcade.gui as arc_gui

from flabbergast.assets import *

from flabbergast import mathematics
from flabbergast import dataproxy
from flabbergast import options


class TooltipOption(options.ImageOption):
    class Scale:
        DEFAULT = 0.44
        ON_HOVER = 0.48

    def __init__(self, *args, **kwargs):
        super().__init__(*args, scale=self.Scale.DEFAULT, **kwargs)


class InputBox(arc_gui.UIInputText):
    class TextureTypeList(Enum):
        DEFAULT = 0
        DOWN = 1

    class Scale:
        DELTA = 0.08
        DEFAULT = 0.55

    class Font:
        COLOR = arc.color.WINE_DREGS
        NAME = "Tekton Display Ssi"
        PATH = assets(FONT_TEKTON)
        SIZE = 22

    EDIT_BUTTON_X_CENTER_X = 0.36

    BOX_OFFSET = 8

    CHAR_LIMIT = 13

    def __init__(self, context, ui_manager, widget_list, center_x, center_y):
        self._context = context

        self._ui_manager = ui_manager

        self._widget_list = widget_list

        self._center_x = center_x
        self._center_y = center_y

        self._background = arc.Sprite(center_x=self._center_x,
                                      center_y=self._center_y,
                                      scale=self.Scale.DEFAULT)
        self._background.textures = [arc.load_texture(assets(WGT_DEFAULT_INPUTBOX)),
                                     arc.load_texture(assets(WGT_DOWN_INPUTBOX))]
        self._background.set_texture(self.TextureTypeList.DEFAULT.value)
        self._widget_list.append(self._background)

        x_offset = self._background.width * self.EDIT_BUTTON_X_CENTER_X
        self._edit_button = TooltipOption([ICON_DEFAULT_EDITPENCIL, ICON_DOWN_EDITPENCIL],
                                          center_x=self._center_x + x_offset,
                                          center_y=self._center_y)
        self._widget_list.append(self._edit_button)
        self._context.events.hover(self._edit_button, self._edit_button.Callback.hover)
        self._context.events.out(self._edit_button, self._edit_button.Callback.out)
        self._context.events.down(self._edit_button, self._edit_button.Callback.down)
        self._context.events.up(self._edit_button, self._edit_button.Callback.up)
        self._context.events.click(self._edit_button, self.on_focus)

        width = self._background.width * (self.Scale.DEFAULT + self.Scale.DELTA)
        height = self._background.height * (self.Scale.DEFAULT + self.Scale.DELTA)
        x = center_x - mathematics.half(width) - self.BOX_OFFSET
        y = center_y - mathematics.half(height) - self.BOX_OFFSET
        super().__init__(text=dataproxy.User.get_name(),
                         x=x,
                         y=y,
                         width=width,
                         height=height,
                         text_color=self.Font.COLOR,
                         font_name=self.Font.NAME,
                         font_size=self.Font.SIZE)

        self._previous_active_state = False
        self._previous_text = self.text

        self._previous_state = None

    def on_update(self, dt):
        super().on_update(dt)

        if self._previous_active_state != self._active:
            if not self._active:
                self.on_blur()
            self._previous_active_state = self._active

        if self._previous_text != self.doc.text:
            self.doc.text = self.doc.text[:self.CHAR_LIMIT]
            self._previous_text = self.doc.text

    def on_focus(self, *args):
        if not self._previous_state:
            self._previous_state = self.doc.text

        self._ui_manager.enable()
        self._active = True
        self.trigger_full_render()
        self.caret.on_activate()
        self.caret.position = len(self.doc.text)
        self._edit_button.visible = False
        self._background.set_texture(self.TextureTypeList.DOWN.value)

    def on_blur(self, *args):
        self._ui_manager.disable()
        self._edit_button.visible = True
        self._background.set_texture(self.TextureTypeList.DEFAULT.value)

    def reset_state(self):
        self._previous_state = None

    def revert_if_unsaved(self):
        if self._previous_state:
            self.doc.text = self._previous_state
            self.trigger_full_render()
