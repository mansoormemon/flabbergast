from pathlib import Path

RESOURCE_PATH = Path(__file__).parent.resolve()


def asset(path):
    return str(RESOURCE_PATH.joinpath(path).resolve())


AUDIO_POP = "audio/pop.mp3"
AUDIO_POSITIVEINTERFACEBEEP = "audio/positiveinterfacebeep.mp3"
AUDIO_POSITIVEINTERFACEHOVER = "audio/positiveinterfacehover.mp3"
AUDIO_WONDROUSWATERS = "audio/wondrouswaters.mp3"

BACKGROUND_MAINMENU = "backgrounds/mainmenu.png"
BACKGROUND_PANE = "backgrounds/pane.png"
BACKGROUND_SETTINGS = "backgrounds/settings.png"

FONT_TEKTON = "fonts/tekton.ttf"

ICON_DEFAULT_EDITPENCIL = "icons/default/editpencil.png"
ICON_DOWN_EDITPENCIL = "icons/down/editpencil.png"

LOGO_CORP = "logos/corporation.png"
LOGO_GAME = "logos/game.png"

MASCOT_CORP = "mascots/corporation.png"

TEAM_FIESTYLION_MASCOT = "teams/fiestylion/mascot.png"
TEAM_LONEWOLF_MASCOT = "teams/lonewolf/mascot.png"

TEAM_SHARED_DEFAULT_MASCOTRING = "teams/shared/default/mascotring.png"
TEAM_SHARED_DOWN_MASCOTRING = "teams/shared/down/mascotring.png"

TEXT_BACK = "text/default/back.png"
TEXT_ENDLESSMODE = "text/default/endlessmode.png"
TEXT_QUIT = "text/default/quit.png"
TEXT_SAVE = "text/default/save.png"
TEXT_SETTINGS = "text/default/settings.png"
TEXT_START = "text/default/start.png"
TEXT_STORYMODE = "text/default/storymode.png"

TEXT_DOWN_BACK = "text/down/back.png"
TEXT_DOWN_ENDLESSMODE = "text/down/endlessmode.png"
TEXT_DOWN_QUIT = "text/down/quit.png"
TEXT_DOWN_SAVE = "text/down/save.png"
TEXT_DOWN_SETTINGS = "text/down/settings.png"
TEXT_DOWN_START = "text/down/start.png"
TEXT_DOWN_STORYMODE = "text/down/storymode.png"

TEXTURES_FLOORGARDEN = "textures/floorgarden.png"

WGT_DEFAULT_ARROWDOWN = "widgets/default/arrowdown.png"
WGT_DEFAULT_ARROWLEFT = "widgets/default/arrowleft.png"
WGT_DEFAULT_ARROWRIGHT = "widgets/default/arrowright.png"
WGT_DEFAULT_ARROWUP = "widgets/default/arrowup.png"
WGT_DEFAULT_INPUTBOX = "widgets/default/inputbox.png"

WGT_DOWN_ARROWDOWN = "widgets/down/arrowdown.png"
WGT_DOWN_ARROWLEFT = "widgets/down/arrowleft.png"
WGT_DOWN_ARROWRIGHT = "widgets/down/arrowright.png"
WGT_DOWN_ARROWUP = "widgets/down/arrowup.png"
WGT_DOWN_INPUTBOX = "widgets/down/inputbox.png"
