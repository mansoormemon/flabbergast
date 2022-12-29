from enum import Enum

import arcade as arc
import arcade.gui as arc_gui

from flabbergast.assets import *

from flabbergast import animations
from flabbergast import avatarmascot
from flabbergast import curtainscene
from flabbergast import dataproxy
from flabbergast import mathematics
from flabbergast import messageconsole
from flabbergast import options
from flabbergast import widgets


class ControlOption(options.TextOption):
    WIDTH = 384

    class FONT:
        FONT = 22

    class Scale(options.TextOption.Scale):
        DEFAULT = 0.6
        ON_HOVER = 0.65

    class Response(options.TextOption.Response):
        VOLUME = 0.3

    def __init__(self, text, *args, **kwargs):
        super().__init__(text, *args, scale=self.Scale.DEFAULT, **kwargs)

    class Callback(options.TextOption.Callback):
        @staticmethod
        def trigger_click_action(context, entity, *args):
            selected_option = Scene.ControlOptionList[entity.get_text().upper()]
            match selected_option:
                case Scene.ControlOptionList.BACK:
                    context.curtains.set_scene(curtainscene.Reference.MAINMENU)
                case Scene.ControlOptionList.SAVE:
                    dataproxy.User.set_team(context.get_mascot().get_current_reference())
                    dataproxy.User.set_name(context.get_player_name_box().text)
                    context.get_mascot().reset_state()
                    context.get_player_name_box().reset_state()
                    dataproxy.User.save()
                    note = arc.Sound(assets(AUDIO_SAVE))
                    note_player = note.play()
                    note.set_volume(entity.Response.VOLUME, note_player)
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

    ARROW_SCALE = 0.36
    ARROW_LEFT_X_LEFT = 0.35
    ARROW_RIGHT_X_LEFT = 0.65

    def __init__(self, *args, **kwargs):
        self._id = None
        self._note = None
        self._background = None
        self._pane = None
        self._interactive_elements = None
        self._lbl_settings = None
        self._control_opts = None
        self._console = None
        self._mascot = None
        self._ui_widgets = None
        self._mascot_arrow_left = None
        self._mascot_arrow_right = None
        self._ui_manager = None
        self._player_name_box = None

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
                                center_y=dataproxy.Meta.screen_height() * self.CONTROL_OPTIONS_Y_BOTTOM)
            self._control_opts.append(opt)
            self.events.hover(opt, opt.Callback.hover)
            self.events.out(opt, opt.Callback.out)
            self.events.down(opt, opt.Callback.down)
            self.events.up(opt, opt.Callback.up)
            self.events.click(
                opt, lambda *args: opt.Callback.trigger_click_action(self, *args)
            )

        # Message console.
        self._console = messageconsole.MessageConsole(self, use_spatial_hash=True)
        for notification in self.ConsoleNotificationList:
            self._console.add_notifier_text(notification.name.title())

        # Avatar mascot.
        self._mascot = avatarmascot.AvatarMascot(dataproxy.Meta.hz_screen_center(),
                                                 dataproxy.Meta.screen_height() * self.MASCOT_Y_BOTTOM)
        self.events.hover(self._mascot.get_ring(), self._mascot.get_ring().Callback.hover)
        self.events.out(self._mascot.get_ring(), self._mascot.get_ring().Callback.out)
        self.events.down(self._mascot.get_ring(), self._mascot.get_ring().Callback.down)
        self.events.up(self._mascot.get_ring(), self._mascot.get_ring().Callback.up)

        # UI widgets.
        self._ui_widgets = arc.SpriteList(use_spatial_hash=True)

        self._mascot_arrow_left = options.NavigationArrow(options.NavigationArrow.Direction.LEFT,
                                                          center_x=dataproxy.Meta.screen_width() * self.ARROW_LEFT_X_LEFT,
                                                          center_y=dataproxy.Meta.screen_height() * self.MASCOT_Y_BOTTOM)
        self._ui_widgets.append(self._mascot_arrow_left)
        self.events.hover(self._mascot_arrow_left, self._mascot_arrow_left.Callback.hover)
        self.events.out(self._mascot_arrow_left, self._mascot_arrow_left.Callback.out)
        self.events.down(self._mascot_arrow_left, self._mascot_arrow_left.Callback.down)
        self.events.up(self._mascot_arrow_left, self._mascot_arrow_left.Callback.up)
        self.events.click(self._mascot_arrow_left, lambda *args: self._mascot.change_avatar(self._mascot.Step.BACK))

        self._mascot_arrow_right = options.NavigationArrow(options.NavigationArrow.Direction.RIGHT,
                                                           center_x=dataproxy.Meta.screen_width() * self.ARROW_RIGHT_X_LEFT,
                                                           center_y=dataproxy.Meta.screen_height() * self.MASCOT_Y_BOTTOM)
        self._ui_widgets.append(self._mascot_arrow_right)
        self.events.hover(self._mascot_arrow_right, self._mascot_arrow_right.Callback.hover)
        self.events.out(self._mascot_arrow_right, self._mascot_arrow_right.Callback.out)
        self.events.down(self._mascot_arrow_right, self._mascot_arrow_right.Callback.down)
        self.events.up(self._mascot_arrow_right, self._mascot_arrow_right.Callback.up)
        self.events.click(self._mascot_arrow_right, lambda *args: self._mascot.change_avatar(self._mascot.Step.FORWARD))

        self._ui_manager = arc_gui.UIManager()

        # Player name label.
        self._player_name_box = widgets.InputBox(self, self._ui_manager, self._ui_widgets,
                                                 dataproxy.Meta.hz_screen_center(),
                                                 dataproxy.Meta.screen_height() * self.PLAYER_NAME_LABEL_Y_BOTTOM)
        self._ui_manager.add(self._player_name_box)

    def get_console(self):
        return self._console

    def get_mascot(self):
        return self._mascot

    def get_player_name_box(self):
        return self._player_name_box

    def draw(self):
        # Draw background.
        self._background.draw_scaled(dataproxy.Meta.hz_screen_center(), dataproxy.Meta.vt_screen_center())

        # Draw pane.
        self._pane.draw_scaled(dataproxy.Meta.hz_screen_center(), dataproxy.Meta.vt_screen_center())

        # Draw sprite lists.
        super().draw()

        # Draw UI manager.
        self._ui_manager.draw()

    def leave_scene(self, next_scene):
        # Reset console.
        self._console.reset()

        # Revert changes if unsaved.
        self._mascot.revert_if_unsaved()
        self._player_name_box.revert_if_unsaved()
