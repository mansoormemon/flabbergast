from __future__ import annotations

from typing import Callable, Optional

import arcade as arc
import arcade.gui as arc_gui

from . import xarcade as xarc
from .assets import (
    AUDIO_POSITIVEINTERFACEBEEP,
    BACKGROUND_SETTINGS,
    BACKGROUND_PANE,
    TEXT_SETTINGS
)
from .assets import asset
from .avatar import Avatar
from .references import SceneList
from .userdata import User

SETTINGS_LABEL_Y: Callable = lambda: xarc.Meta.screen_height() * 0.8

CONTROL_OPTIONS_Y: Callable = lambda: xarc.Meta.screen_height() * 0.2

AVATAR_Y: Callable = lambda: xarc.Meta.screen_height() * 0.55

PLAYER_NAME_BOX_Y: Callable = lambda: xarc.Meta.screen_height() * 0.32


class ControlOptionList(xarc.Reference):
    BACK = 0
    SAVE = 1


class ConsoleNotificationList(xarc.Reference):
    SAVED = "Changes Saved!"


class ControlOption(xarc.TextOption):
    WIDTH: int = 384

    class Scale(xarc.TextOption.Scale):
        DEFAULT: float = 0.6
        ON_HOVER: float = 0.65

    class Response(xarc.TextOption.Response):
        VOLUME: float = 0.3

    def __init__(self, text: str, *args, scale: float = Scale.DEFAULT, **kwargs):
        super().__init__(text, *args, scale=scale, **kwargs)

    def click(self, context: SettingsPane, *args):
        selected_option: ControlOptionList = ControlOptionList[self.text.upper()]
        match selected_option:
            case ControlOptionList.BACK:
                context.curtains.set_scene(SceneList.MAINMENU)
            case ControlOptionList.SAVE:
                User.set_team(context.avatar.team.data)
                User.set_name(context.player_name_box.text)
                context.avatar.flush()
                context.player_name_box.flush()
                User.save()
                note: arc.Sound = arc.Sound(asset(AUDIO_POSITIVEINTERFACEBEEP))
                note_player: arc.sound.media.Player = note.play()
                note.set_volume(self.Response.VOLUME, note_player)
                context.console.trigger_notification(ConsoleNotificationList.SAVED)

    def connect(self, context: SettingsPane, *_):
        super().connect(context)
        context.events.click(self, lambda *args: self.click(context, *args))


class SettingsPane(xarc.AbstractScene):
    def __init__(self, *args, **kwargs):
        self.background: Optional[arc.Texture] = None
        self.pane: Optional[arc.Texture] = None
        self.interactive_elements: Optional[arc.SpriteList] = None
        self.lbl_settings: Optional[arc.Sprite] = None
        self.control_opts: Optional[arc.SpriteList] = None
        self.console: Optional[xarc.MessageConsole] = None
        self.avatar: Optional[Avatar] = None
        self.ui_widgets: Optional[arc.SpriteList] = None
        self.avatar_arrow_left: Optional[xarc.NavigationArrow] = None
        self.avatar_arrow_right: Optional[xarc.NavigationArrow] = None
        self.ui_manager: Optional[arc_gui.UIManager] = None
        self.player_name_box: Optional[xarc.ui.InputBox] = None

        super().__init__(SceneList.SETTINGSPANE, *args, **kwargs)

    def setup(self):
        self.background = arc.load_texture(asset(BACKGROUND_SETTINGS))

        self.pane = arc.load_texture(asset(BACKGROUND_PANE))

        self.interactive_elements = arc.SpriteList(use_spatial_hash=True)

        self.lbl_settings = arc.Sprite(asset(TEXT_SETTINGS),
                                       center_x=xarc.Meta.hz_screen_center(),
                                       center_y=SETTINGS_LABEL_Y())
        self.events.hover(self.lbl_settings,
                          lambda entity, *_: self.animations.fire(entity,
                                                                  xarc.Animation.inflate(entity.scale)))
        self.events.out(self.lbl_settings,
                        lambda entity, *_: self.animations.fire(entity,
                                                                xarc.Animation.deflate(entity.scale)))
        self.interactive_elements.append(self.lbl_settings)

        self.control_opts = arc.SpriteList(use_spatial_hash=True)
        x_disp_offset: float = (len(ControlOptionList) - 1) * ControlOption.WIDTH * 0.5
        for n, opt in enumerate(ControlOptionList):
            ctrl_opt = ControlOption(opt.as_key(),
                                     center_x=xarc.Meta.hz_screen_center() + (n * ControlOption.WIDTH) - x_disp_offset,
                                     center_y=CONTROL_OPTIONS_Y())
            ctrl_opt.connect(self)
            self.control_opts.append(ctrl_opt)

        self.console = xarc.MessageConsole(self, use_spatial_hash=True)
        for notification in ConsoleNotificationList:
            self.console.add(notification, notification.value)

        self.avatar = Avatar(xarc.Meta.hz_screen_center(), AVATAR_Y())
        self.avatar.connect(self)

        self.ui_widgets = arc.SpriteList(use_spatial_hash=True)

        self.ui_manager = arc_gui.UIManager()

        self.player_name_box = xarc.ui.InputBox(User.get_name(),
                                                self.ui_manager,
                                                self.ui_widgets,
                                                xarc.Meta.hz_screen_center(),
                                                PLAYER_NAME_BOX_Y())
        self.player_name_box.connect(self)
        self.ui_manager.add(self.player_name_box)

    def leave_scene(self, next_scene: xarc.AbstractScene):
        self.console.reset()

        # Revert unsaved changes.
        self.avatar.stabilize()
        self.player_name_box.stabilize()

    def draw(self):
        self.background.draw_scaled(xarc.Meta.hz_screen_center(), xarc.Meta.vt_screen_center())
        self.pane.draw_scaled(xarc.Meta.hz_screen_center(), xarc.Meta.vt_screen_center())

        super().draw()

        self.ui_manager.draw()

    def on_update(self, delta_time: float):
        self.console.on_update(delta_time)

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case arc.key.ESCAPE:
                self.curtains.set_scene(SceneList.MAINMENU)
