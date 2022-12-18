from enum import Enum

import arcade as arc
import arcade_curtains as arc_curts

from flabbergast.animations import *
from flabbergast.assets import *
from flabbergast.metadata import *
from flabbergast.optionsprite import *
from flabbergast.scenes import *
from flabbergast.util import *


class ControlOption(OptionSprite):
    WIDTH = 384

    class Scale:
        DEFAULT = 0.6
        ON_HOVER = 0.65

    def __init__(self, text, *args, **kwargs):
        super().__init__(text, *args, **kwargs)

    class Callback(OptionSprite.Callback):
        @staticmethod
        def trigger_click_action(scene, entity, *args):
            selected_option = SettingsMenu.ControlOptionList[entity.get_text().upper()]
            match selected_option:
                case SettingsMenu.ControlOptionList.BACK:
                    scene.curtains.set_scene(Scene.MAIN_MENU)
                case SettingsMenu.ControlOptionList.SAVE:
                    note = arc.Sound(assets(AUDIO_SAVE))
                    note_player = note.play()
                    note.set_volume(entity.Volume.RESPONSE_NOTE, note_player)


class SettingsMenu(NamedScene):
    class ControlOptionList(Enum):
        BACK = 0
        SAVE = 1

    SETTINGS_LABEL_Y_BOTTOM = 0.75
    CONTROL_OPTIONS_Y_BOTTOM = 0.25

    def __init__(self, *args, **kwargs):
        self._id = None
        self._background = None
        self._pane = None
        self._interactive_elements = None
        self._lbl_settings = None
        self._control_opts = None

        super().__init__(Scene.SETTINGS, *args, **kwargs)

    def setup(self):
        # Static contents.
        self._background = arc.load_texture(assets(BACKGROUND_SETTINGS))
        self._pane = arc.load_texture(assets(BACKGROUND_PANE))

        # Interactive elements.
        self._interactive_elements = arc.SpriteList(use_spatial_hash=True)

        self._lbl_settings = arc.Sprite(assets(TEXT_SETTINGS))
        self._lbl_settings.center_x = Metadata.hz_screen_center()
        self._lbl_settings.center_y = Metadata.screen_height() * self.SETTINGS_LABEL_Y_BOTTOM
        self.events.hover(self._lbl_settings, Animation.inflate)
        self.events.out(self._lbl_settings, Animation.deflate)
        self._interactive_elements.append(self._lbl_settings)

        # Control options.
        self._control_opts = arc.SpriteList(use_spatial_hash=True)
        x_disp_offset = half((len(self.ControlOptionList) - 1) * ControlOption.WIDTH)
        for n, opt in enumerate(self.ControlOptionList):
            opt = ControlOption(opt.name.lower(), scale=ControlOption.Scale.DEFAULT)
            opt.center_x = Metadata.hz_screen_center() + (n * ControlOption.WIDTH) - x_disp_offset
            opt.center_y = Metadata.screen_height() * self.CONTROL_OPTIONS_Y_BOTTOM

            self.events.hover(opt, ControlOption.Callback.hover)
            self.events.out(opt, ControlOption.Callback.out)
            self.events.down(opt, ControlOption.Callback.down)
            self.events.up(opt, ControlOption.Callback.up)
            self.events.click(
                opt, lambda *args: ControlOption.Callback.trigger_click_action(self, *args)
            )

            self._control_opts.append(opt)

    def draw(self):
        # Draw background.
        self._background.draw_scaled(Metadata.hz_screen_center(), Metadata.vt_screen_center())

        # Draw pane.
        self._pane.draw_scaled(Metadata.hz_screen_center(), Metadata.vt_screen_center())

        # Draw sprite lists.
        super().draw()
