from enum import Enum

import arcade as arc
import arcade_curtains as arc_curts

from flabbergast.assets import *

from flabbergast import animations
from flabbergast import curtainscene
from flabbergast import dataproxy
from flabbergast import options


class MenuOption(options.TextOption):
    HEIGHT = 96

    def __init__(self, text, *args, **kwargs):
        super().__init__(text, *args, scale=self.Scale.DEFAULT, **kwargs)

    class Callback(options.TextOption.Callback):
        @staticmethod
        def trigger_click_action(context, entity, *args):
            selected_option = Scene.OptionList[entity.get_text().upper()]
            match selected_option:
                case Scene.OptionList.START:
                    context.curtains.set_scene(curtainscene.Reference.PLATFORMER)
                case Scene.OptionList.SETTINGS:
                    context.curtains.set_scene(curtainscene.Reference.SETTINGSPANE)
                case Scene.OptionList.QUIT:
                    dataproxy.User.save()
                    arc.exit()


class Scene(curtainscene.AbstractScene):
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
        self._id = None
        self._first_visit = None
        self._sound = None
        self._sound_player = None
        self._background = None
        self._logo_corp = None
        self._mascot_corp = None
        self._interactive_elements = None
        self._logo_game = None
        self._menu_opts = None

        super().__init__(curtainscene.Reference.MAINMENU, *args, **kwargs)

    def setup(self):
        # Set flag for first visit.
        self._first_visit = True

        # Set background music.
        self._sound = arc.load_sound(assets(AUDIO_BACKGROUND_MAINMENU), True)

        # Static contents.
        self._background = arc.load_texture(assets(BACKGROUND_MAINMENU))
        self._logo_corp = arc.load_texture(assets(LOGO_CORP))
        self._mascot_corp = arc.load_texture(assets(MASCOT_CORP))

        # Interactive contents.
        self._interactive_elements = arc.SpriteList(use_spatial_hash=True)

        self._logo_game = arc.Sprite(assets(LOGO_GAME),
                                     center_x=dataproxy.Meta.hz_screen_center(),
                                     center_y=dataproxy.Meta.screen_height() * self.LOGO_GAME_Y_BOTTOM)
        self._interactive_elements.append(self._logo_game)
        self.events.hover(self._logo_game,
                          lambda entity, *args: self.animations.fire(entity,
                                                                     animations.Animation.inflate(entity.scale)))
        self.events.out(self._logo_game,
                        lambda entity, *args: self.animations.fire(entity,
                                                                   animations.Animation.deflate(entity.scale)))

        # Menu options.
        self._menu_opts = arc.SpriteList(use_spatial_hash=True)
        for n, opt in enumerate(self.OptionList):
            opt = MenuOption(opt.name.lower(),
                             center_x=dataproxy.Meta.hz_screen_center(),
                             center_y=(dataproxy.Meta.vt_screen_center()
                                       - (n * MenuOption.HEIGHT)
                                       + (dataproxy.Meta.screen_height() * self.MENU_OPTIONS_Y_CENTER)),
                             )
            opt.alpha = animations.Alpha.INVISIBLE
            self._menu_opts.append(opt)

    def draw(self):
        # Draw background.
        self._background.draw_scaled(dataproxy.Meta.hz_screen_center(), dataproxy.Meta.vt_screen_center())

        # Draw corporation logo.
        self._logo_corp.draw_scaled(dataproxy.Meta.screen_width() * self.LOGO_CORP_X_LEFT,
                                    dataproxy.Meta.screen_height() * self.LOGO_CORP_Y_BOTTOM)

        # Draw corporation mascot.
        self._mascot_corp.draw_scaled(dataproxy.Meta.screen_width() * self.MASCOT_CORP_X_LEFT,
                                      dataproxy.Meta.screen_height() * self.MASCOT_CORP_Y_BOTTOM)

        # Draw sprite lists.
        super().draw()

    def connect_menu_option_events(self, entity):
        self.events.hover(entity, entity.Callback.hover)
        self.events.out(entity, entity.Callback.out)
        self.events.down(entity, entity.Callback.down)
        self.events.up(entity, entity.Callback.up)
        self.events.click(entity,
                          lambda *args: entity.Callback.trigger_click_action(self, *args))

    def enter_scene(self, previous_scene):
        # Fire logo animation on first visit.
        if self._first_visit:
            fade_in_logo = animations.Animation.fade_in_with_pause(speed=animations.Speed.DEFAULT)
            logo_animation = (self._logo_game, fade_in_logo)

            menu_opts_animation = [
                (
                    opt, animations.Animation.fade_in(speed=animations.Speed.VERY_FAST,
                                                      callback=(self.connect_menu_option_events, opt))
                )
                for opt in self._menu_opts
            ]

            chain = arc_curts.Chain()
            chain.add_sequences(logo_animation, *menu_opts_animation)
            self.animations.fire(None, chain)

        # Play background music.
        self._sound_player = arc.play_sound(self._sound, looping=True)

        # Update first visit flag.
        self._first_visit = False

    def leave_scene(self, next_scene):
        # Stop background music.
        arc.stop_sound(self._sound_player)
