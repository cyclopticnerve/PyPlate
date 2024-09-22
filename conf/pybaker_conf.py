# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pybaker_conf.py                                       |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
This module separates out the constants from pybaker.py.
This file, and the template folder, are the main ways to customize PyPlate.
"""

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

S_ERR_PRJ_DIR_NO_EXIST = "Project dir {} does not exist"
S_ERR_PRJ_DIR_NONE = "Project dir not provided"

S_DST = "dist"
S_CHANGELOG = "CHANGELOG.md"
S_CHANGELOG_CMD = "git log --pretty='%ad - %s'"

S_TOML_VERSION_SEARCH = (
    r"(^\s*\[project\]\s*$)(.*?)(^\s*version[\t ]*=[\t ]*)(.*?$)"
)
S_TOML_VERSION_REPL = r'\g<1>\g<2>\g<3>"{}"'
S_TOML_SHORT_DESC_SEARCH = (
    r"(^\s*\[project\]\s*$)(.*?)(^\s*description[\t ]*=[\t ]*)(.*?$)"
)
S_TOML_SHORT_DESC_REPL = r'\g<1>\g<2>\g<3>"{}"'
S_TOML_KW_SEARCH = (
    r"(^\s*\[project\]\s*$)(.*?)(^\s*keywords[\t ]*=[\t ]*)(.*?\])"
)
S_TOML_KW_REPL = r"\g<1>\g<2>\g<3>[{}]"

S_META_VER_SEARCH = r"(\s*__PB_VERSION__\s*=\s*)(.*)"
S_META_VER_REPL = r'\g<1>"{}"'
S_META_SD_SEARCH = r"(\s*__PB_SHORT_DESC__\s*=\s*)(.*)"
S_META_SD_REPL = r'\g<1>"{}"'

# ------------------------------------------------------------------------------

# S_ERR_COUNT = "Errors: {}"
# S_ERR_UFNF = "ERROR: File {} could not be found, trying default"
# S_ERR_UJSON = "ERROR: FIle {} is not a valid JSON file, trying default"
# S_ERR_DFNF = "ERROR: Default file {} could not be found"
# S_ERR_DJSON = "ERROR: Default file {} is not a valid JSON file"

# ------------------------------------------------------------------------------
# Lists
# ------------------------------------------------------------------------------

L_SRC = [
    "conf",
    "README",
    "src",
    "LICENSE.txt",
    "README.md",
]

# get list of approved categories
# https://specifications.freedesktop.org/menu-spec/latest/apa.html
L_CATS = [
    "AudioVideo",
    "Audio",
    "Video",
    "Development",
    "Education",
    "Game",
    "Graphics",
    "Network",
    "Office",
    "Science",
    "Settings",
    "System",
    "Utility",
    "Building",
    "Debugger",
    "IDE",
    "GUIDesigner",
    "Profiling",
    "RevisionControl",
    "Translation",
    "Calendar",
    "ContactManagement",
    "Database",
    "Dictionary",
    "Chart",
    "Email",
    "Finance",
    "FlowChart",
    "PDA",
    "ProjectManagement",
    "Presentation",
    "Spreadsheet",
    "WordProcessor",
    "2DGraphics",
    "VectorGraphics",
    "RasterGraphics",
    "3DGraphics",
    "Scanning",
    "OCR",
    "Photography",
    "Publishing",
    "Viewer",
    "TextTools",
    "DesktopSettings",
    "HardwareSettings",
    "Printing",
    "PackageManager",
    "Dialup",
    "InstantMessaging",
    "Chat",
    "IRCClient",
    "Feed",
    "FileTransfer",
    "HamRadio",
    "News",
    "P2P",
    "RemoteAccess",
    "Telephony",
    "TelephonyTools",
    "VideoConference",
    "WebBrowser",
    "WebDevelopment",
    "Midi",
    "Mixer",
    "Sequencer",
    "Tuner",
    "TV",
    "AudioVideoEditing",
    "Player",
    "Recorder",
    "DiscBurning",
    "ActionGame",
    "AdventureGame",
    "ArcadeGame",
    "BoardGame",
    "BlocksGame",
    "CardGame",
    "KidsGame",
    "LogicGame",
    "RolePlaying",
    "Shooter",
    "Simulation",
    "SportsGame",
    "StrategyGame",
    "Art",
    "Construction",
    "Music",
    "Languages",
    "ArtificialIntelligence",
    "Astronomy",
    "Biology",
    "Chemistry",
    "ComputerScience",
    "DataVisualization",
    "Economy",
    "Electricity",
    "Geography",
    "Geology",
    "Geoscience",
    "History",
    "Humanities",
    "ImageProcessing",
    "Literature",
    "Maps",
    "Math",
    "NumericalAnalysis",
    "MedicalSoftware",
    "Physics",
    "Robotics",
    "Spirituality",
    "Sports",
    "ParallelComputing",
    "Amusement",
    "Archiving",
    "Compression",
    "Electronics",
    "Emulator",
    "Engineering",
    "FileTools",
    "FileManager",
    "TerminalEmulator",
    "Filesystem",
    "Monitor",
    "Security",
    "Accessibility",
    "Calculator",
    "Clock",
    "TextEditor",
    "Documentation",
    "Adult",
    "Core",
    "KDE",
    "GNOME",
    "XFCE",
    "DDE",
    "GTK",
    "Qt",
    "Motif",
    "Java",
    "ConsoleOnly",
    "Screensaver",
    "TrayIcon",
    "Applet",
    "Shell",
]
