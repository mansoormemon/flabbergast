import arcade as arc
import arcade_curtains as arc_curts

from flabbergast.animations import *
from flabbergast.arithmetic import *
from flabbergast.assets import *
from flabbergast.metadata import *
from flabbergast.optionsprite import *
from flabbergast.scenes import *
from flabbergast.util import *


class MenuOption(OptionSprite):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

    class Callback(OptionSprite.Callback):
        @staticmethod
        def trigger_action(scene, entity, *args):
            match entity.name:
                case MainMenu.OPTION_START:
                    scene.curtains.set_scene(Scene.LEVEL)
                case MainMenu.OPTION_SETTINGS:
                    scene.curtains.set_scene(Scene.SETTINGS)
                case MainMenu.OPTION_QUIT:
                    arc.exit()


class MainMenu(arc_curts.BaseScene):
    GAME_LOGO_Y = 0.8

    CORP_LOGO_Y = 0.08
    CORP_LOGO_DISP_X_LEFT = 0.8

    OPTION_START = "Start"
    OPTION_SETTINGS = "Settings"
    OPTION_QUIT = "Quit"
    OPTIONS = [OPTION_START, OPTION_SETTINGS, OPTION_QUIT]

    MENU_DISP_Y_CENTER = 0.08

    def setup(self):
        self._first_visit = True

        # Set background music.
        self.sound = arc.load_sound(assets(MUSIC_BACKGROUND_MAIN_MENU), True)
        self.sound_player = None

        # Static contents.
        self._static_contents = arc.SpriteList(use_spatial_hash=True)

        background = arc.Sprite(assets(BACKGROUND_MAIN_MENU))
        background.center_x = Metadata.hz_screen_center()
        background.center_y = Metadata.vt_screen_center()
        self._static_contents.append(background)

        corp_logo = arc.Sprite(assets(CORP_LOGO))
        corp_logo.center_x = Metadata.screen_width() * self.CORP_LOGO_DISP_X_LEFT
        corp_logo.center_y = Metadata.screen_height() * self.CORP_LOGO_Y
        self._static_contents.append(corp_logo)

        self._game_logo = arc.Sprite(assets(GAME_LOGO))
        self._game_logo.center_x = Metadata.hz_screen_center()
        self._game_logo.center_y = Metadata.screen_height() * self.GAME_LOGO_Y
        self.events.hover(self._game_logo, Animation.inflate)
        self.events.out(self._game_logo, Animation.deflate)
        self._static_contents.append(self._game_logo)

        # Menu options.
        self._menu_opts = arc.SpriteList(use_spatial_hash=True)
        for n, opt in enumerate(self.OPTIONS):
            opt = MenuOption(
                opt, assets(f"{TEXT_DIR}/{opt}.png"), scale=MenuOption.Scale.DEFAULT
            )
            opt.center_x = Metadata.hz_screen_center()
            opt.center_y = (
                Metadata.vt_screen_center()
                - (n * MenuOption.V_PADDING)
                + (Metadata.screen_height() * self.MENU_DISP_Y_CENTER)
            )

            self.events.hover(opt, MenuOption.Callback.hover)
            self.events.out(opt, MenuOption.Callback.out)
            self.events.down(opt, MenuOption.Callback.down)
            self.events.up(opt, MenuOption.Callback.up)
            self.events.click(
                opt, lambda *args: MenuOption.Callback.trigger_action(self, *args)
            )

            self._menu_opts.append(opt)

    def enter_scene(self, previous_scene):
        # Fire logo animation on first visit.
        if self._first_visit:
            ANIMATION_FRAME_DURATION = 2

            logo_anim_seq = arc_curts.Sequence()
            logo_anim_frames = [
                arc_curts.KeyFrame(scale=half(self._game_logo.scale)),
                arc_curts.KeyFrame(scale=self._game_logo.scale),
            ]

            for n, frame in enumerate(logo_anim_frames):
                logo_anim_seq.add_keyframe(n * ANIMATION_FRAME_DURATION, frame)

            self.animations.fire(self._game_logo, logo_anim_seq)

        # Play background music.
        self.sound_player = arc.play_sound(self.sound, looping=True)

        self._first_visit = False

    def leave_scene(self, next_scene):
        # Stop background music.
        arc.stop_sound(self.sound_player)
