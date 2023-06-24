<!----------------------------------------------------------------------------->
<!-- Project : PyPlate                                         /          \  -->
<!-- Filename: metadata.md                                    |     ()     | -->
<!-- Date    : 12/19/2022                                     |            | -->
<!-- Author  : cyclopticnerve                                 |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

# Metadata.json

You should edit this file by hand before running 'metadata.py'.

This the basic structure of 'metadata.json':

```
{
    "PP_VERSION": "0.1.0",
    "PP_SHORT_DESC": "A program for creating module/package/CLI/GUI projects in Python from a template",
    "PP_KEYWORDS": "python,cli,template,app,package,gui,module,gtk3",
    "PP_PY_DEPS": {
        "numpy", "https://numpy.org/",
    },
    "PP_SYS_DEPS": "",
    "PP_GUI_CATEGORIES": ""
}
```
## PP_VERSION

This is the canonical (only and absolute) version number string for this
project. This should provide the absolute version number string (in [semantic
notation](https://semver.org/)) of this project, and all other version numbers
should be superseded by this string.

## PP_SHORT_DESC

This is the short description of the project, used in 'README.md'
and 'pyproject.toml', as well as the GUI "About" dialog.

## PP_KEYWORDS

These are the keywords for the project, for use in 'pyproject.toml' for the 
PyPI listing, and should also be used in the GitHub project page. Delimiters 
for all entries MUST be a comma (unless you edit this in pyplate.py).

## PP_PY_DEPS

These are the python dependencies for the project. They are stored here for
'install.py', 'pyproject.toml', and 'README.md.' It is a dictionary where the
key is the dependency name, and the value is a link to some web page (for
'README.md'). When used in 'pyproject.toml' or 'install.py', it will be
automatically downloaded by pip using just the dependency name.

## PP_SYS_DEPS

These are the system dependencies for the project, i.e non-python dependencies. 
They are stored here for 'install.py.' Delimiters for all entries MUST be a 
comma (unless you edit this in pyplate.py).

## PP_GUI_CATEGORIES

These are the categories used in the '.desktop' file of a GUI program, to 
present in a menu-based Desktop UI (think windows start menu grouping).

Each entry must match an entry in the following list:
```
LIST_CATEGORIES = [
    'AudioVideo',
    'Audio',
    'Video',
    'Development',
    'Education',
    'Game',
    'Graphics',
    'Network',
    'Office',
    'Science',
    'Settings',
    'System',
    'Utility',
    'Building',
    'Debugger',
    'IDE',
    'GUIDesigner',
    'Profiling',
    'RevisionControl',
    'Translation',
    'Calendar',
    'ContactManagement',
    'Database',
    'Dictionary',
    'Chart',
    'Email',
    'Finance',
    'FlowChart',
    'PDA',
    'ProjectManagement',
    'Presentation',
    'Spreadsheet',
    'WordProcessor',
    '2DGraphics',
    'VectorGraphics',
    'RasterGraphics',
    '3DGraphics',
    'Scanning',
    'OCR',
    'Photography',
    'Publishing',
    'Viewer',
    'TextTools',
    'DesktopSettings',
    'HardwareSettings',
    'Printing',
    'PackageManager',
    'Dialup',
    'InstantMessaging',
    'Chat',
    'IRCClient',
    'Feed',
    'FileTransfer',
    'HamRadio',
    'News',
    'P2P',
    'RemoteAccess',
    'Telephony',
    'TelephonyTools',
    'VideoConference',
    'WebBrowser',
    'WebDevelopment',
    'Midi',
    'Mixer',
    'Sequencer',
    'Tuner',
    'TV',
    'AudioVideoEditing',
    'Player',
    'Recorder',
    'DiscBurning',
    'ActionGame',
    'AdventureGame',
    'ArcadeGame',
    'BoardGame',
    'BlocksGame',
    'CardGame',
    'KidsGame',
    'LogicGame',
    'RolePlaying',
    'Shooter',
    'Simulation',
    'SportsGame',
    'StrategyGame',
    'Art',
    'Construction',
    'Music',
    'Languages',
    'ArtificialIntelligence',
    'Astronomy',
    'Biology',
    'Chemistry',
    'ComputerScience',
    'DataVisualization',
    'Economy',
    'Electricity',
    'Geography',
    'Geology',
    'Geoscience',
    'History',
    'Humanities',
    'ImageProcessing',
    'Literature',
    'Maps',
    'Math',
    'NumericalAnalysis',
    'MedicalSoftware',
    'Physics',
    'Robotics',
    'Spirituality',
    'Sports',
    'ParallelComputing',
    'Amusement',
    'Archiving',
    'Compression',
    'Electronics',
    'Emulator',
    'Engineering',
    'FileTools',
    'FileManager',
    'TerminalEmulator',
    'Filesystem',
    'Monitor',
    'Security',
    'Accessibility',
    'Calculator',
    'Clock',
    'TextEditor',
    'Documentation',
    'Adult',
    'Core',
    'KDE',
    'GNOME',
    'XFCE',
    'DDE',
    'GTK',
    'Qt',
    'Motif',
    'Java',
    'ConsoleOnly',
    'Screensaver',
    'TrayIcon',
    'Applet',
    'Shell',
]
```

If the entry does not match, it will be igmored.

## -)
<!-- -) -->
