from __future__ import annotations

from typing import Callable, Optional

import arcade as arc
import arcade.gui as arc_gui

from . import xarcade as xarc
from .assets import (
    AUDIO_POSITIVEINTERFACEBEEP,
    BACKGROUND_SETTINGS,
    TEXT_DEFAULT_SETTINGS
)
from .assets import asset
from .avatar import Avatar
from .controlspane import ControlsPane
from .references import SceneList
from .userdata import User

AVATAR_Y: Callable = lambda: xarc.Meta.screen_height() * 0.55

PLAYER_NAME_BOX_Y: Callable = lambda: xarc.Meta.screen_height() * 0.32


class ConsoleNotificationList(xarc.Reference):
    SAVED = "Changes Saved!"


class SettingsPane(ControlsPane):
    class ControlOptionList(xarc.Reference):
        BACK = 0
        SAVE = 1

    class ControlOption(ControlsPane.ControlOption):
        def click(self, context: SettingsPane, *args):
            selected_option: context.ControlOptionList = context.ControlOptionList[self.text.upper()]
            match selected_option:
                case context.ControlOptionList.BACK:
                    context.curtains.set_scene(SceneList.MAINMENU)
                case context.ControlOptionList.SAVE:
                    User.set_team(context.avatar.team.data)
                    User.set_name(context.player_name_box.text)
                    context.avatar.flush()
                    context.player_name_box.flush()
                    User.save()
                    note: arc.Sound = arc.Sound(asset(AUDIO_POSITIVEINTERFACEBEEP))
                    note_player: arc.sound.media.Player = note.play()
                    note.set_volume(self.Response.VOLUME, note_player)
                    context.console.trigger_notification(ConsoleNotificationList.SAVED)

    def __init__(self, *args, **kwargs):
        self.console: Optional[xarc.MessageConsole] = None
        self.avatar: Optional[Avatar] = None
        self.ui_widgets: Optional[arc.SpriteList] = None
        self.avatar_arrow_left: Optional[xarc.NavigationArrow] = None
        self.avatar_arrow_right: Optional[xarc.NavigationArrow] = None
        self.ui_manager: Optional[arc_gui.UIManager] = None
        self.player_name_box: Optional[xarc.ui.InputBox] = None

        super().__init__(SceneList.SETTINGSPANE, *args, **kwargs)

    def setup(self, *args, **kwargs):
        super().setup(heading=TEXT_DEFAULT_SETTINGS, background=BACKGROUND_SETTINGS)

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
        super().draw()

        self.ui_manager.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case arc.key.ESCAPE:
                self.curtains.set_scene(SceneList.MAINMENU)

    def on_update(self, delta_time: float):
        self.console.on_update(delta_time)
