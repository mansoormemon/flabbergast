import arcade as arc
import arcade_curtains as arc_curts

from flabbergast.animations import *
from flabbergast.assets import *
from flabbergast.metadata import *
from flabbergast.optionsprite import *
from flabbergast.scenes import *
from flabbergast.util import *


class ControlOption(OptionSprite):
    class Scale:
        DEFAULT = 0.6
        HOVER = 0.65

    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

    class Callback(OptionSprite.Callback):
        @staticmethod
        def trigger_action(scene, entity, *args):
            match entity.name:
                case SettingsMenu.CONTROL_BACK:
                    scene.curtains.set_scene(Scene.MAIN_MENU)
                case SettingsMenu.CONTROL_SAVE:
                    print("saved")


class SettingsMenu(arc_curts.BaseScene):
    SETTINGS_LABEL_Y = 0.75
    CONTROLS_Y = 0.25

    CONTROL_BACK = "Back"
    CONTROL_SAVE = "Save"
    CONTROLS = [CONTROL_BACK, CONTROL_SAVE]

    def setup(self):
        # Static contents.
        self._static_contents = arc.SpriteList(use_spatial_hash=True)

        background = arc.Sprite(assets(BACKGROUND_SETTINGS))
        background.center_x = Metadata.hz_screen_center()
        background.center_y = Metadata.vt_screen_center()
        self._static_contents.append(background)

        settings_pane = arc.Sprite(assets(BACKGROUND_PANE))
        settings_pane.center_x = Metadata.hz_screen_center()
        settings_pane.center_y = Metadata.vt_screen_center()
        self._static_contents.append(settings_pane)

        settings_label = arc.Sprite(assets(TEXT_SETTINGS))
        settings_label.center_x = Metadata.hz_screen_center()
        settings_label.center_y = Metadata.screen_height() * self.SETTINGS_LABEL_Y
        self.events.hover(settings_label, Animation.inflate)
        self.events.out(settings_label, Animation.deflate)
        self._static_contents.append(settings_label)

        # Control options.
        self._controls = arc.SpriteList(use_spatial_hash=True)
        for n, opt in enumerate(self.CONTROLS):
            opt = ControlOption(
                opt, assets(f"{TEXT_DIR}/{opt}.png"), scale=ControlOption.Scale.DEFAULT
            )
            opt.center_x = (
                Metadata.hz_screen_center()
                + (n * ControlOption.H_PADDING)
                + half(len(self.CONTROLS) * ControlOption.H_PADDING)
            )
            opt.center_y = Metadata.screen_height() * self.CONTROLS_Y

            self.events.hover(opt, ControlOption.Callback.hover)
            self.events.out(opt, ControlOption.Callback.out)
            self.events.down(opt, ControlOption.Callback.down)
            self.events.up(opt, ControlOption.Callback.up)
            self.events.click(
                opt, lambda *args: ControlOption.Callback.trigger_action(self, *args)
            )

            self._controls.append(opt)
