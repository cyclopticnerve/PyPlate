<!----------------------------------------------------------------------------->
<!-- Project : PyPlate                                         /          \  -->
<!-- Filename: README.md                                      |     ()     | -->
<!-- Date    : 12/19/2022                                     |            | -->
<!-- Author  : cyclopticnerve                                 |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

# PyPlate

## "It mostly works™"
[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/about/)

<!-- __RM_SHORT_DESC_START__ -->
A program for creating module/package/CLI/GUI projects in Python from a template
<!-- __RM_SHORT_DESC_END__ -->

<!-- ![Screenshot](README/screenshot.jpg) -->

## Requirements
<!-- __RM_PY_DEPS_START__ -->
None
<!-- __RM_PY_DEPS_END__ -->

## Installing
You can download the (hopefully stable)
[latest release](https://github.com/cyclopticnerve/PyPlate/releases/latest) 
from the main branch.<br>
Download either the 'tar.gz' or 'zip' file and extract it.<br>
Rename the folder without the version, e.g. 'PyPlate-0.1.0' to 'PyPlate'.

Or you can clone the git repo to get the latest (and often broken) code from the
dev branch:
```bash
foo@bar:~$ cd ~/Downloads
foo@bar:~/Downloads$ git clone https://github.com/cyclopticnerve/PyPlate
```

Next, cut/copy/paste the 'PyPlate' directory wherever you want. For the examples
below, we will use '~/Documents/Projects/Python/'.
```bash
foo@bar:~/Downloads$ mv PyPlate ~/Documents/Projects/Python
```

Lastly, you can delete the downloaded folder, if you copied it.

## Uninstalling
Just delete the 'PyPlate' folder from wherever you put it in the install step.

## Usage
PyPlate consists of two scripts, 'pyplate.py' and 'metadata.py'. The first is 
used to create the project, and the second is used to update an existing project 
as its development continues.

Let us start with 'pyplate.py'.
<hr>

## PyPlate.py
Before you do anything, you should edit the 'user.json' file in 'PyPlate/conf'. 
This file contains your personal information that is used when creating a new 
project. The fields should be pretty self-explanatory, but here is a brief 
description of each:

### PP_DATE_FMT
The date format to use in headers

### PP_AUTHOR
The name to use for 'Author' in headers and pyproject.toml

### PP_EMAIL
The email address to use in headers and pyproject.toml

### PP_LICENSE
The license to use in headers and pyproject.toml

To create a project, cd into the 'PyPlate/src/' directory, and run 'pyplate.py':
``` bash
foo@bar:~$ cd ~/Documents/Projects/Python/PyPlate/src
foo@bar:~/Documents/Projects/Python/PyPlate/src$ ./pyplate.py
```

Enter the required information, and 'pyplate.py' will create the required files
and folders in a subdirectory of 'DIR_BASE', where 'DIR_BASE' is the directory
above 'PyPlate'. In our example, 'DIR_BASE' is '~/Documents/Projects/Python'.

Modules/Packages will be generated in '~/Documents/Projects/Python/Libs', and
CLI/GUI apps will be generated in '~/Documents/Projects/Python/Apps'.

From there you are free to modify the projects in your favorite IDE.

Once your project is ready for release, run the 'metadata.py' file from the 
project's 'conf' directory. This will update any metadata you have added/edited 
in the 'conf' directory.

<hr>

## Metadata.py / Customizing the project
Once you have created a project, you can use 'metadata.py' in the project's 
'conf' directory to update metada in the project's files.

'metadata.py' is a script which will replace certain keywords in the project 
directory. These keywords are placed in files in the 'conf' directory of your 
project. These files are explained below.

The files in the 'conf' directory can be edited at any time (except 
'settings.json'), followed by re-running 'metadata.py'. The script uses 
regular expressions to search for context (i.e. text before and after the 
replacement) so as long as the context does not change, 'metadata.py' can 
replace text at any time. 


## Blacklist.json
You should edit this file by hand before running 'metadata.py'. This file is
used by 'metadata.py' to determine which files/folders it can (or rather, 
*can't*) operate on.

Files in the new project are divided, internally, into four cateigories:
1. the file's COMPLETE contents
2. the file's headers
3. the file's text (other that the header)
4. the path to the file

The default 'blacklist.json' file should look something like this:

```
{
    "skip_all": [
        ".venv",
        ".git",
        "dist",
        "docs",
        "misc",
        "tests",
        "__pycache__",
        "PKG-INFO",
        "locale"
    ],
    "skip_file": [
        "__PP_NAME_SMALL__.png"
    ],
    "skip_header": [],
    "skip_text": [
        "metadata.py",
        "settings.json",
        "strings.json"
    ],
    "skip_path": []
}
```

The individual entries are:

### skip_all
A list of folders/files for which NOTHING should be done. Don't fix headers, 
text, or path. Leave them untouched.

This section is usually used for files/folders which DO NOT belong to you, or 
are auto-generated outside your project.

### skip_file
'metadata.py' may fix the path, but not the internal contents of the file.

This is equivalent to placing the same file in both 
'skip_header' and 'skip_text'.

This section is used for things like images, where the contents of the file are 
not text.

##### skip_header
'metadata.py' may fix the contents of the file, as well as the path, but not the 
header contents.

This section is rarely used.

### skip_text
'metadata.py' may fix the header, as well as the path, but not the other
contents of the file.

This section is commonly used for config files where the
header should match the project, but the contents should not be altered. 

*Note that 'skip_text' should ALWAYS include 'metadata.py', 'settings.json', 
and 'strings.json', and should NEVER include 'blacklist.json'. This is because 
these files have certain keywords which need to be replaced (or not replaced) 
in order for 'metadata.py'. function correctly.*

### skip_path
'metadata.py' may fix the header, as well as the contents, but not the path of 
the file.

This section is rarely used.

## Strings.json
You should edit this file by hand before running 'metadata.py'. This file is
used by 'metadata.py' to determine what strings should be replaced in the
project.

This is a sample structure of 'strings.json':

```
{
    "PP_VERSION": "0.1.0",
    "PP_SHORT_DESC": "A program for creating module/package/CLI/GUI projects in Python from a template",
    "PP_KEYWORDS": ["key", "word"],
    "PP_PY_DEPS": {
        "numpy", "https://numpy.org/",
    },
    "PP_SYS_DEPS": ["dep1", "dep2"],
    "PP_GUI_CATEGORIES": ["cat1", "cat2"]
}
```

The individual entries are:

### PP_VERSION
This is the canonical (only and absolute) version number string for this
project. This should provide the absolute version number string (in [semantic
notation](https://semver.org/)) of this project, and all other version numbers
should be superseded by this string. Value is a string.

### PP_SHORT_DESC
This is the short description of the project, used in 'README.md'
and 'pyproject.toml', as well as the GUI "About" dialog. Value is a string.

### PP_KEYWORDS
This is an array of keywords for the project, for use in 'pyproject.toml' for
the PyPI listing, and should also be used in the GitHub project page. Value is
an array, with each value quoted, and separated by a comma.

### PP_PY_DEPS
This is an array of Python dependencies for the project. They are stored here
for 'install.py', 'pyproject.toml', and 'README.md.' It is a dictionary where
the key is the dependency name, and the value is a link to some web page (for
'README.md'). When used in 'pyproject.toml' or 'install.py', it will be
automatically downloaded by pip using just the dependency name.

### PP_SYS_DEPS
This is an array of system dependencies for the project, i.e non-python
dependencies. They are stored here for 'install.py.'  Value is an array, with
each value quoted, and separated by a comma.

### PP_GUI_CATEGORIES
This is an array of categories used in the '.desktop' file of a GUI program, to
present in a menu-based Desktop UI (think windows start menu grouping). Value is
an array, with each value separated by a semiquote, and must end with semiquote.  

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

If the entry does not match, it will be ignored, and an error will be printed.

## Settings.json

You should NOT edit this file by hand. It is created when PyPlate creates a new 
project, and the dictionary is filled automatically. This file is used by 
'metadata.py' to get the initial project settings.

It is explained here only to show what it contains.

This the basic structure of 'settings.json':

```
{
    "project": {
        "type": "m"
    },
    "info": {
        "__PP_NAME_BIG__": "ModTest",
        "__PP_NAME_SMALL__": "modtest",
        "__PP_DATE__": "06/23/2023"
    }
}
```

## Project

### Type

Indicates the type of project, "m" for module, "p" for package, "c" for CLI, 
and "g" for GTK GUI.

 ## Info

 ### \_\_PP_NAME_BIG__

 The properly capitalized name of the project, for use in strings displayed to 
 the user.

 ### \_\_PP_NAME_SMALL__

 The lowecase version of the project name, used internally by PyPlate and 
 metadata.py.

  ### \_\_PP_DATE__

  The date the project was created, used internally by PyPlate and metada.py.

<hr>

After these files have been edited appropriately, run 'metadata.py' from the
'conf' directory to update the metadata in the project. This module can be run
any time AFTER the project has been created to update the metadata in the
project. Here is an example for a project of type 'm' (module) named 'ModTest':

``` bash
foo@bar:~$ cd ~/Documents/Projects/Python/Libs/ModTest/conf
foo@bar:~/Documents/Projects/Python/Libs/ModTest/conf$ ./metadata.py
```

'modtext.py' will print any errors it finds, along with the filename and line 
number, so you can correct them.

## Notes
If you make any changes to this template to better suit your own style/setup, 
please let me know or send a pull request. I will take a look and see if I can 
incorporate your changes to make them user-agnostic. This way the template can 
hopefully become more customizable to suit everyone's needs.

## -)
<!-- -) -->
