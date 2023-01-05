from enum import Enum

import arcade as arc
import arcade_curtains as arc_curts

from .assets import asset
from .dataproxy import Meta, User
from .references import SceneList

from .assets import (
    AUDIO_WONDROUSWATERS,
    BACKGROUND_MAINMENU,
    LOGO_CORP,
    LOGO_GAME,
    MASCOT_CORP
)

from . import xarcade as xarc


class MenuOption(xarc.TextOption):
    HEIGHT = 96

    class Callback(xarc.TextOption.Callback):
        @staticmethod
        def click(context, entity, *args):
            selected_option = MainMenu.OptionList[entity.get_text().upper()]
            match selected_option:
                case MainMenu.OptionList.START:
                    context.curtains.set_scene(SceneList.CUTSCENE)
                case MainMenu.OptionList.SETTINGS:
                    context.curtains.set_scene(SceneList.SETTINGSPANE)
                case MainMenu.OptionList.QUIT:
                    User.save()
                    arc.exit()


class MainMenu(xarc.AbstractScene):
    class OptionList(Enum):
        START = 0
        SETTINGS = 1
        QUIT = 2

    LOGO_CORP_Y_BOTTOM = 0.05
    LOGO_CORP_X_LEFT = 0.85

    MASCOT_CORP_Y_BOTTOM = 0.06
    MASCOT_CORP_X_LEFT = 0.04

    LOGO_GAME_Y_BOTTOM = 0.8

    MENU_OPTIONS_Y_CENTER = 0.08

    def __init__(self, *args, **kwargs):
        self._first_visit = None
        self._sound = None
        self._sound_player = None
        self._background = None
        self._logo_corp = None
        self._mascot_corp = None
        self._interactive_elements = None
        self._logo_game = None
        self._menu_opts = None

        super().__init__(SceneList.MAINMENU, *args, **kwargs)

    def setup(self):
        # Set flag for first visit.
        self._first_visit = True

        # Set background music.
        self._sound = arc.load_sound(asset(AUDIO_WONDROUSWATERS), True)

        # Static contents.
        self._background = arc.load_texture(asset(BACKGROUND_MAINMENU))
        self._logo_corp = arc.load_texture(asset(LOGO_CORP))
        self._mascot_corp = arc.load_texture(asset(MASCOT_CORP))

        # Interactive contents.
        self._interactive_elements = arc.SpriteList(use_spatial_hash=True)

        self._logo_game = arc.Sprite(asset(LOGO_GAME),
                                     center_x=Meta.hz_screen_center(),
                                     center_y=Meta.screen_height() * self.LOGO_GAME_Y_BOTTOM)
        self._interactive_elements.append(self._logo_game)
        self.events.hover(self._logo_game,
                          lambda entity, *args: self.animations.fire(entity,
                                                                     xarc.Animation.inflate(entity.scale)))
        self.events.out(self._logo_game,
                        lambda entity, *args: self.animations.fire(entity,
                                                                   xarc.Animation.deflate(entity.scale)))

        # Menu options.
        self._menu_opts = arc.SpriteList(use_spatial_hash=True)
        for n, opt in enumerate(self.OptionList):
            opt = MenuOption(opt.name.lower(),
                             center_x=Meta.hz_screen_center(),
                             center_y=(Meta.vt_screen_center()
                                       - (n * MenuOption.HEIGHT)
                                       + (Meta.screen_height() * self.MENU_OPTIONS_Y_CENTER)),
                             )
            opt.alpha = xarc.Alpha.INVISIBLE
            self._menu_opts.append(opt)

    def draw(self):
        self._background.draw_scaled(Meta.hz_screen_center(), Meta.vt_screen_center())

        self._logo_corp.draw_scaled(Meta.screen_width() * self.LOGO_CORP_X_LEFT,
                                    Meta.screen_height() * self.LOGO_CORP_Y_BOTTOM)

        self._mascot_corp.draw_scaled(Meta.screen_width() * self.MASCOT_CORP_X_LEFT,
                                      Meta.screen_height() * self.MASCOT_CORP_Y_BOTTOM)

        super().draw()

    def connect_menu_option_events(self, entity):
        self.events.hover(entity, entity.Callback.hover)
        self.events.out(entity, entity.Callback.out)
        self.events.down(entity, entity.Callback.down)
        self.events.up(entity, entity.Callback.up)
        self.events.click(entity,
                          lambda *args: entity.Callback.click(self, *args))

    def enter_scene(self, previous_scene):
        # Fire logo animation on first visit.
        if self._first_visit:
            fade_in_logo = xarc.Animation.fade_in_with_delay(speed=xarc.Speed.DEFAULT)
            logo_animation = (self._logo_game, fade_in_logo)

            menu_opts_animation = [
                (
                    opt, xarc.Animation.fade_in(speed=xarc.Speed.VERY_FAST,
                                                callback=(self.connect_menu_option_events, opt))
                )
                for opt in self._menu_opts
            ]

            chain = arc_curts.Chain()
            chain.add_sequences(logo_animation, *menu_opts_animation)
            self.animations.fire(None, chain)

        self._sound_player = arc.play_sound(self._sound, looping=True)

        # Update first visit flag.
        self._first_visit = False

    def leave_scene(self, next_scene):
        arc.stop_sound(self._sound_player)
