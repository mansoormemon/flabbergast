from flabbergast import util

DIR_ASSETS = "assets"


def get_assets_folder():
    return util.get_project_root().joinpath(DIR_ASSETS)


def assets(path):
    return str(get_assets_folder().joinpath(path))


FMT_IMAGE = "png"
FMT_AUDIO = "mp3"
FMT_FONT = "ttf"

DIR_AUDIO = "audio"
DIR_BACKGROUNDS = "backgrounds"
DIR_FONTS = "fonts"
DIR_FRAMES = "frames"
DIR_LOGOS = "logos"
DIR_MASCOTS = "mascots"
DIR_TEAMS = "teams"
DIR_TEXT = "text"
DIR_TEXTURES = "textures"
DIR_WIDGETS = "widgets"

AUDIO_BACKGROUND_MAINMENU = f"{DIR_AUDIO}/wondrouswaters.{FMT_AUDIO}"
AUDIO_LONGPOP = f"{DIR_AUDIO}/longpop.{FMT_AUDIO}"
AUDIO_MOUSE_HOVER_RESPONSE = f"{DIR_AUDIO}/positiveinterfacehover.{FMT_AUDIO}"
AUDIO_SAVE = f"{DIR_AUDIO}/positiveinterfacebeep.{FMT_AUDIO}"

BACKGROUND_MAINMENU = f"{DIR_BACKGROUNDS}/mainmenu.{FMT_IMAGE}"
BACKGROUND_PANE = f"{DIR_BACKGROUNDS}/pane.{FMT_IMAGE}"
BACKGROUND_SETTINGS = f"{DIR_BACKGROUNDS}/settings.{FMT_IMAGE}"

FONT_TEKTON = f"{DIR_FONTS}/tekton.{FMT_FONT}"

LOGO_CORP = f"{DIR_LOGOS}/corporation.{FMT_IMAGE}"
LOGO_GAME = f"{DIR_LOGOS}/game.{FMT_IMAGE}"

MASCOT_CORP = f"{DIR_MASCOTS}/corporation.{FMT_IMAGE}"

TEAM_FIESTYLION_MASCOT = f"{DIR_TEAMS}/fiestylion/mascot.{FMT_IMAGE}"
TEAM_LONEWOLF_MASCOT = f"{DIR_TEAMS}/lonewolf/mascot.{FMT_IMAGE}"

TEAM_SHARED_DEFAULT_MASCOTRING = f"{DIR_TEAMS}/shared/default/mascotring.{FMT_IMAGE}"
TEAM_SHARED_DOWN_MASCOTRING = f"{DIR_TEAMS}/shared/down/mascotring.{FMT_IMAGE}"

TEXT_BACK = f"{DIR_TEXT}/default/back.{FMT_IMAGE}"
TEXT_ENDLESSMODE = f"{DIR_TEXT}/default/endlessmode.{FMT_IMAGE}"
TEXT_QUIT = f"{DIR_TEXT}/default/quit.{FMT_IMAGE}"
TEXT_SAVE = f"{DIR_TEXT}/default/save.{FMT_IMAGE}"
TEXT_SETTINGS = f"{DIR_TEXT}/default/settings.{FMT_IMAGE}"
TEXT_START = f"{DIR_TEXT}/default/start.{FMT_IMAGE}"
TEXT_STORYMODE = f"{DIR_TEXT}/default/storymode.{FMT_IMAGE}"

TEXT_DOWN_BACK = f"{DIR_TEXT}/down/back.{FMT_IMAGE}"
TEXT_DOWN_ENDLESSMODE = f"{DIR_TEXT}/down/endlessmode.{FMT_IMAGE}"
TEXT_DOWN_QUIT = f"{DIR_TEXT}/down/quit.{FMT_IMAGE}"
TEXT_DOWN_SAVE = f"{DIR_TEXT}/down/save.{FMT_IMAGE}"
TEXT_DOWN_SETTINGS = f"{DIR_TEXT}/down/settings.{FMT_IMAGE}"
TEXT_DOWN_START = f"{DIR_TEXT}/down/start.{FMT_IMAGE}"
TEXT_DOWN_STORYMODE = f"{DIR_TEXT}/down/storymode.{FMT_IMAGE}"

TEXTURES_FLOORGARDEN = f"{DIR_TEXTURES}/floorgarden.{FMT_IMAGE}"

WGT_DEFAULT_INPUTBOX = f"{DIR_WIDGETS}/default/inputbox.{FMT_IMAGE}"
WGT_DOWN_INPUTBOX = f"{DIR_WIDGETS}/down/inputbox.{FMT_IMAGE}"
