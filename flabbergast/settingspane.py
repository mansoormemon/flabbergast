from enum import Enum

import arcade as arc

from flabbergast.assets import *

from flabbergast import animations
from flabbergast import avatarmascot
from flabbergast import curtainscene
from flabbergast import dataproxy
from flabbergast import mathematics
from flabbergast import messageconsole
from flabbergast import option


class ControlOption(option.Option):
    WIDTH = 384

    class FONT:
        FONT = 22

    class Scale:
        DEFAULT = 0.6
        ON_HOVER = 0.65

    def __init__(self, text, *args, **kwargs):
        super().__init__(text, *args, **kwargs)

    class Callback(option.Option.Callback):
        @staticmethod
        def trigger_click_action(context, entity, *args):
            selected_option = Scene.ControlOptionList[entity.get_text().upper()]
            match selected_option:
                case Scene.ControlOptionList.BACK:
                    context.curtains.set_scene(curtainscene.Reference.MAINMENU)
                case Scene.ControlOptionList.SAVE:
                    note = arc.Sound(assets(AUDIO_SAVE))
                    note_player = note.play()
                    note.set_volume(entity.Volume.RESPONSE_NOTE, note_player)
                    context.get_console().trigger_notification(context,
                                                               Scene.ConsoleNotificationList.SAVED.name.title())


class Scene(curtainscene.AbstractScene):
    class ControlOptionList(Enum):
        BACK = 0
        SAVE = 1

    class ConsoleNotificationList(Enum):
        SAVED = 0

    SETTINGS_LABEL_Y_BOTTOM = 0.8

    CONTROL_OPTIONS_Y_BOTTOM = 0.2

    MASCOT_Y_BOTTOM = 0.55

    PLAYER_NAME_LABEL_Y_BOTTOM = 0.32
    PLAYER_NAME_LABEL_SCALE = 0.44

    FONT_COLOR = arc.color.WINE_DREGS
    FONT_NAME = "Tekton Display Ssi"
    FONT_SIZE = 22

    def __init__(self, *args, **kwargs):
        self._id = None
        self._background = None
        self._pane = None
        self._interactive_elements = None
        self._lbl_settings = None
        self._control_opts = None
        self._console = None
        self._mascot = None
        self._ui_widgets = None
        self._player_name = None

        super().__init__(curtainscene.Reference.SETTINGSPANE, *args, **kwargs)

    def setup(self):
        # Static contents.
        self._background = arc.load_texture(assets(BACKGROUND_SETTINGS))
        self._pane = arc.load_texture(assets(BACKGROUND_PANE))

        # Interactive elements.
        self._interactive_elements = arc.SpriteList(use_spatial_hash=True)

        self._lbl_settings = arc.Sprite(assets(TEXT_SETTINGS),
                                        center_x=dataproxy.Meta.hz_screen_center(),
                                        center_y=dataproxy.Meta.screen_height() * self.SETTINGS_LABEL_Y_BOTTOM)
        self._interactive_elements.append(self._lbl_settings)
        self.events.hover(self._lbl_settings,
                          lambda entity, *args: self.animations.fire(entity,
                                                                     animations.Animation.inflate(entity.scale)))
        self.events.out(self._lbl_settings,
                        lambda entity, *args: self.animations.fire(entity,
                                                                   animations.Animation.deflate(entity.scale)))

        # Control options.
        self._control_opts = arc.SpriteList(use_spatial_hash=True)

        x_disp_offset = mathematics.half((len(self.ControlOptionList) - 1) * ControlOption.WIDTH)
        for n, opt in enumerate(self.ControlOptionList):
            opt = ControlOption(opt.name.lower(),
                                center_x=dataproxy.Meta.hz_screen_center() + (n * ControlOption.WIDTH) - x_disp_offset,
                                center_y=dataproxy.Meta.screen_height() * self.CONTROL_OPTIONS_Y_BOTTOM,
                                scale=ControlOption.Scale.DEFAULT)
            self._control_opts.append(opt)

            self.events.hover(opt, ControlOption.Callback.hover)
            self.events.out(opt, ControlOption.Callback.out)
            self.events.down(opt, ControlOption.Callback.down)
            self.events.up(opt, ControlOption.Callback.up)
            self.events.click(
                opt, lambda *args: opt.Callback.trigger_click_action(self, *args)
            )

        # Message console.
        self._console = messageconsole.MessageConsole(self, use_spatial_hash=True)
        for notification in self.ConsoleNotificationList:
            self._console.add_notifier_text(notification.name.title())

        # Avatar mascot.
        self._mascot = avatarmascot.AvatarMascot(avatarmascot.Reference[dataproxy.User.get_team().upper()],
                                                 center_x=dataproxy.Meta.hz_screen_center(),
                                                 center_y=dataproxy.Meta.screen_height() * self.MASCOT_Y_BOTTOM)
        self.events.hover(self._mascot.get_ring(), self._mascot.Callback.hover)
        self.events.out(self._mascot.get_ring(), self._mascot.Callback.out)
        self.events.down(self._mascot.get_ring(), self._mascot.Callback.down)
        self.events.up(self._mascot.get_ring(), self._mascot.Callback.up)

        # UI widgets.
        self._ui_widgets = arc.SpriteList(use_spatial_hash=True)

        # Player name label.
        self._player_name = arc.Sprite(assets(WGT_DEFAULT_INPUTBOX),
                                       center_x=dataproxy.Meta.hz_screen_center(),
                                       center_y=dataproxy.Meta.screen_height() * self.PLAYER_NAME_LABEL_Y_BOTTOM,
                                       scale=self.PLAYER_NAME_LABEL_SCALE)
        self._ui_widgets.append(self._player_name)

    def get_console(self):
        return self._console

    def draw(self):
        # Draw background.
        self._background.draw_scaled(dataproxy.Meta.hz_screen_center(), dataproxy.Meta.vt_screen_center())

        # Draw pane.
        self._pane.draw_scaled(dataproxy.Meta.hz_screen_center(), dataproxy.Meta.vt_screen_center())

        # Draw sprite lists.
        super().draw()

        # Draw player's name.
        arc.draw_text(dataproxy.User.get_name(),
                      self._player_name.center_x,
                      self._player_name.center_y,
                      color=self.FONT_COLOR,
                      font_size=self.FONT_SIZE, font_name=self.FONT_NAME,
                      anchor_x="center", anchor_y="center")

    def leave_scene(self, next_scene):
        # Reset console.
        self._console.reset()
