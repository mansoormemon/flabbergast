from __future__ import annotations

from typing import Callable, List, Optional, Tuple

import arcade as arc
import arcade_curtains as arc_curts

from . import xarcade as xarc
from .assets import (
    AUDIO_WONDROUSWATERS,
    BACKGROUND_MAINMENU,
    LOGO_GAME,
    LOGO_CORP,
    MASCOT_CORP
)
from .assets import asset
from .references import SceneList

LOGO_CORP_Y: Callable = lambda: xarc.Meta.screen_height() * 0.05
LOGO_CORP_X: Callable = lambda: xarc.Meta.screen_width() * 0.85

MASCOT_CORP_Y: Callable = lambda: xarc.Meta.screen_height() * 0.06
MASCOT_CORP_X: Callable = lambda: xarc.Meta.screen_width() * 0.04

LOGO_GAME_Y: Callable = lambda: xarc.Meta.screen_height() * 0.8

MENU_OPTIONS_Y_CENTER: Callable = lambda: xarc.Meta.vt_screen_center() * 0.08


class OptionList(xarc.Reference):
    START = 0
    SETTINGS = 1
    QUIT = 2


class MenuOption(xarc.TextOption):
    HEIGHT: int = 96

    def click(self, context: MainMenu, *_):
        selected_option: OptionList = OptionList[self.text.upper()]
        if selected_option == OptionList.START:
            context.curtains.set_scene(SceneList.SELECTMODEPANE)
        elif selected_option == OptionList.SETTINGS:
            context.curtains.set_scene(SceneList.SETTINGSPANE)
        elif selected_option == OptionList.QUIT:
            arc.exit()

    def connect(self, context: MainMenu, *_):
        super().connect(context)
        context.events.click(self, lambda *args: self.click(context, *args))


class MainMenu(xarc.AbstractScene):
    def __init__(self, *args, **kwargs):
        self.first_visit: Optional[bool] = None
        self.sound: Optional[arc.Sound] = None
        self.sound_player: Optional[arc.sound.media.Player] = None
        self.background: Optional[arc.Texture] = None
        self.logo_corp: Optional[arc.Texture] = None
        self.mascot_corp: Optional[arc.Texture] = None
        self.interactive_elements: Optional[arc.SpriteList] = None
        self.logo_game: Optional[arc.Sprite] = None
        self.menu_opts: Optional[arc.SpriteList] = None

        super().__init__(SceneList.MAINMENU, *args, **kwargs)

    def setup(self, *args, **kwargs):
        self.first_visit = True

        self.sound = arc.load_sound(asset(AUDIO_WONDROUSWATERS), True)

        self.background = arc.load_texture(asset(BACKGROUND_MAINMENU))

        self.logo_corp = arc.load_texture(asset(LOGO_CORP))

        self.mascot_corp = arc.load_texture(asset(MASCOT_CORP))

        self.interactive_elements = arc.SpriteList(use_spatial_hash=True)

        self.logo_game = arc.Sprite(asset(LOGO_GAME),
                                    center_x=xarc.Meta.hz_screen_center(),
                                    center_y=LOGO_GAME_Y())
        self.events.hover(self.logo_game,
                          lambda entity, *_: self.animations.fire(entity,
                                                                  xarc.Animation.inflate(entity.scale)))
        self.events.out(self.logo_game,
                        lambda entity, *_: self.animations.fire(entity,
                                                                xarc.Animation.deflate(entity.scale)))
        self.interactive_elements.append(self.logo_game)

        self.menu_opts = arc.SpriteList(use_spatial_hash=True)
        for n, opt in enumerate(OptionList):
            menu_opt: MenuOption = MenuOption(opt.as_key(),
                                              center_x=xarc.Meta.hz_screen_center(),
                                              center_y=(xarc.Meta.vt_screen_center()
                                                        - (n * MenuOption.HEIGHT)
                                                        + MENU_OPTIONS_Y_CENTER()))
            menu_opt.alpha = xarc.Alpha.INVISIBLE
            self.menu_opts.append(menu_opt)

    def enter_scene(self, previous_scene: xarc.AbstractScene):
        if self.first_visit:
            fade_in_logo: arc_curts.Sequence = xarc.Animation.fade_in_with_delay(speed=xarc.Speed.DEFAULT)
            logo_animation: Tuple[arc.Sprite, arc_curts.Sequence] = (self.logo_game, fade_in_logo)

            menu_opts_animation: List[Tuple[MenuOption, arc_curts.Sequence]] = [
                (
                    menu_opt, xarc.Animation.fade_in(speed=xarc.Speed.VERY_FAST,
                                                     callback=(menu_opt.connect, self))
                )
                for menu_opt in self.menu_opts
            ]

            chain: arc_curts.Chain = arc_curts.Chain()
            chain.add_sequences(logo_animation, *menu_opts_animation)
            self.animations.fire(None, chain)

        self.sound_player = arc.play_sound(self.sound, looping=True)

        self.first_visit = False

    def leave_scene(self, next_scene: xarc.AbstractScene):
        arc.stop_sound(self.sound_player)

    def draw(self):
        self.background.draw_scaled(xarc.Meta.hz_screen_center(), xarc.Meta.vt_screen_center())
        self.logo_corp.draw_scaled(LOGO_CORP_X(), LOGO_CORP_Y())
        self.mascot_corp.draw_scaled(MASCOT_CORP_X(), MASCOT_CORP_Y())

        super().draw()
