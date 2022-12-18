import arcade as arc
import arcade_curtains as arc_curts

from flabbergast.animations import *
from flabbergast.assets import *
from flabbergast.metadata import *
from flabbergast.optionsprite import *
from flabbergast.scenes import *
from flabbergast.util import *


class MenuOption(OptionSprite):
    HEIGHT = 96

    def __init__(self, text, *args, **kwargs):
        super().__init__(text, *args, **kwargs)

    class Callback(OptionSprite.Callback):
        @staticmethod
        def trigger_click_action(scene, entity, *args):
            selected_option = MainMenu.OptionList[entity.get_text().upper()]
            match selected_option:
                case MainMenu.OptionList.START:
                    scene.curtains.set_scene(Scene.LEVEL)
                case MainMenu.OptionList.SETTINGS:
                    scene.curtains.set_scene(Scene.SETTINGS)
                case MainMenu.OptionList.QUIT:
                    arc.exit()


class MainMenu(NamedScene):
    class OptionList(Enum):
        START = 0
        SETTINGS = 1
        QUIT = 2

    LOGO_CORP_Y_BOTTOM = 0.08
    LOGO_CORP_X_LEFT = 0.8

    LOGO_GAME_Y_BOTTOM = 0.8

    MENU_OPTIONS_Y_CENTER = 0.08

    def __init__(self, *args, **kwargs):
        self._id = None
        self._first_visit = None
        self._sound = None
        self._sound_player = None
        self._background = None
        self._logo_corp = None
        self._interactive_elements = None
        self._logo_game = None
        self._menu_opts = None

        super().__init__(Scene.MAIN_MENU, *args, **kwargs)

    def setup(self):
        # Set flag for first visit.
        self._first_visit = True

        # Set background music.
        self._sound = arc.load_sound(assets(AUDIO_BACKGROUND_MAIN_MENU), True)

        # Static contents.
        self._background = arc.load_texture(assets(BACKGROUND_MAIN_MENU))
        self._logo_corp = arc.load_texture(assets(LOGO_CORP_GLOW))

        # Interactive contents.
        self._interactive_elements = arc.SpriteList(use_spatial_hash=True)

        self._logo_game = arc.Sprite(assets(LOGO_GAME))
        self._logo_game.center_x = Metadata.hz_screen_center()
        self._logo_game.center_y = Metadata.screen_height() * self.LOGO_GAME_Y_BOTTOM
        self.events.hover(self._logo_game, Animation.inflate)
        self.events.out(self._logo_game, Animation.deflate)
        self._interactive_elements.append(self._logo_game)

        # Menu options.
        self._menu_opts = arc.SpriteList(use_spatial_hash=True)
        for n, opt in enumerate(self.OptionList):
            opt = MenuOption(opt.name.lower(), scale=MenuOption.Scale.DEFAULT)
            opt.center_x = Metadata.hz_screen_center()
            opt.center_y = (
                    Metadata.vt_screen_center()
                    - (n * MenuOption.HEIGHT)
                    + (Metadata.screen_height() * self.MENU_OPTIONS_Y_CENTER)
            )
            opt.alpha = Alpha.INVISIBLE

            self._menu_opts.append(opt)

    def draw(self):
        # Draw background.
        self._background.draw_scaled(Metadata.hz_screen_center(), Metadata.vt_screen_center())

        # Draw corporation logo.
        self._logo_corp.draw_scaled(Metadata.screen_width() * self.LOGO_CORP_X_LEFT,
                                    Metadata.screen_height() * self.LOGO_CORP_Y_BOTTOM)

        # Draw sprite lists.
        super().draw()

    def connect_menu_option_events(self, entity):
        self.events.hover(entity, MenuOption.Callback.hover)
        self.events.out(entity, MenuOption.Callback.out)
        self.events.down(entity, MenuOption.Callback.down)
        self.events.up(entity, MenuOption.Callback.up)
        self.events.click(
            entity, lambda *args: MenuOption.Callback.trigger_click_action(self, *args)
        )

    def enter_scene(self, previous_scene):
        # Fire logo animation on first visit.
        if self._first_visit:
            fade_in_logo = AnimationSequence.fade_in_with_pause(speed=Speed.FAST)
            logo_animation = (self._logo_game, fade_in_logo)

            menu_opts_animation = []
            for opt in self._menu_opts:
                fade_in_menu_opts = AnimationSequence.fade_in(speed=Speed.VERY_FAST,
                                                              callback_func=(self.connect_menu_option_events, opt))
                menu_opts_animation.append((opt, fade_in_menu_opts))

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
