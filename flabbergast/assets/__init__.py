from pathlib import Path

RESOURCE_PATH: Path = Path(__file__).parent.resolve()


def asset(path: str) -> str:
    return str(RESOURCE_PATH.joinpath(path).resolve())


AUDIO_KEYBOARDTYPING: str = "audio/keyboardtyping.mp3"
AUDIO_POP: str = "audio/pop.mp3"
AUDIO_POSITIVEINTERFACEBEEP: str = "audio/positiveinterfacebeep.mp3"
AUDIO_POSITIVEINTERFACEHOVER: str = "audio/positiveinterfacehover.mp3"
AUDIO_QUICKWARNINGNOTIFICATION: str = "audio/quickwarningnotification.mp3"
AUDIO_THEREISAPATTERN: str = "audio/thereisapattern.mp3"
AUDIO_WONDROUSWATERS: str = "audio/wondrouswaters.mp3"

BACKGROUND_ARBITRARY_1: str = "images/backgrounds/arbitrary/1.png"
BACKGROUND_ARBITRARY_2: str = "images/backgrounds/arbitrary/2.png"
BACKGROUND_ARBITRARY_3: str = "images/backgrounds/arbitrary/3.png"
BACKGROUND_ARBITRARY_0: str = "images/backgrounds/arbitrary/0.png"
BACKGROUND_ENDLESS: str = "images/backgrounds/endless.png"
BACKGROUND_MAINMENU: str = "images/backgrounds/mainmenu.png"
BACKGROUND_PANE: str = "images/backgrounds/pane.png"
BACKGROUND_SELECTMODE: str = "images/backgrounds/selectmode.png"
BACKGROUND_SETTINGS: str = "images/backgrounds/settings.png"
BACKGROUND_STORY: str = "images/backgrounds/story.png"

CUTSCENE_OPENING: str = "cutscenes/openingscene.json"

FONT_TEKTON: str = "fonts/tekton.ttf"

ICON_DEFAULT_EDITPENCIL: str = "images/icons/default/editpencil.png"
ICON_DOWN_EDITPENCIL: str = "images/icons/down/editpencil.png"

LOGO_GAME: str = "images/logos/game.png"
LOGO_CORP: str = "images/logos/corporation.png"

MASCOT_CORP: str = "images/mascots/corporation.png"

TEAM_FIESTYLION_MASCOT: str = "images/teams/fiestylion/mascot.png"
TEAM_LONEWOLF_MASCOT: str = "images/teams/lonewolf/mascot.png"

TEAM_SHARED_DEFAULT_MASCOTRING: str = "images/teams/shared/default/mascotring.png"
TEAM_SHARED_DOWN_MASCOTRING: str = "images/teams/shared/down/mascotring.png"

TEXT_DEFAULT_BACK: str = "images/text/default/back.png"
TEXT_DEFAULT_ENDLESS: str = "images/text/default/endless.png"
TEXT_DEFAULT_QUIT: str = "images/text/default/quit.png"
TEXT_DEFAULT_SAVE: str = "images/text/default/save.png"
TEXT_DEFAULT_SETTINGS: str = "images/text/default/settings.png"
TEXT_DEFAULT_START: str = "images/text/default/start.png"
TEXT_DEFAULT_STORY: str = "images/text/default/story.png"
TEXT_DEFAULT_SELECTMODE: str = "images/text/default/selectmode.png"

TEXT_DOWN_BACK: str = "images/text/down/back.png"
TEXT_DOWN_ENDLESS: str = "images/text/down/endlessmode.png"
TEXT_DOWN_QUIT: str = "images/text/down/quit.png"
TEXT_DOWN_SAVE: str = "images/text/down/save.png"
TEXT_DOWN_SETTINGS: str = "images/text/down/settings.png"
TEXT_DOWN_START: str = "images/text/down/start.png"
TEXT_DOWN_STORY: str = "images/text/down/storymode.png"
TEXT_DOWN_SELECTMODE: str = "images/text/down/selectmode.png"

WGT_DEFAULT_ARROWDOWN: str = "images/widgets/default/arrowdown.png"
WGT_DEFAULT_ARROWLEFT: str = "images/widgets/default/arrowleft.png"
WGT_DEFAULT_ARROWRIGHT: str = "images/widgets/default/arrowright.png"
WGT_DEFAULT_ARROWUP: str = "images/widgets/default/arrowup.png"
WGT_DEFAULT_INPUTBOX: str = "images/widgets/default/inputbox.png"

WGT_DOWN_ARROWDOWN: str = "images/widgets/down/arrowdown.png"
WGT_DOWN_ARROWLEFT: str = "images/widgets/down/arrowleft.png"
WGT_DOWN_ARROWRIGHT: str = "images/widgets/down/arrowright.png"
WGT_DOWN_ARROWUP: str = "images/widgets/down/arrowup.png"
WGT_DOWN_INPUTBOX: str = "images/widgets/down/inputbox.png"
