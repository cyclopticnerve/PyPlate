<!----------------------------------------------------------------------------->
<!-- Project : PyPlate                                         /          \  -->
<!-- Filename: README.md                                      |     ()     | -->
<!-- Date    : 12/19/2022                                     |            | -->
<!-- Author  : cyclopticnerve                                 |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

# PyPlate

## "It mostly works™"

[![License: WTFPLv2](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/about/)

A program for creating CLI/Package/GUI projects in Python from a template

## Requirements
None

## Installing
You can download the (hopefully stable) [latest
release](https://github.com/cyclopticnerve/PyPlate/releases/latest) from the
main branch.<br>
Download either the 'tar.gz' or 'zip' file and extract it.<br>
Go into the extracted folder and run the installer.
```bash
cd ~/Documents/Downloads/PyPlate-<version>$ ./install.sh
```

Rename the folder without the version, e.g. 'PyPlate-0.1.0' to 'PyPlate'.

Or you can clone the git repo to get the latest (and often broken) code from the
dev branch:
```bash
foo@bar:~$ cd ~/Downloads
foo@bar:~/Downloads$ git clone https://github.com/cyclopticnerve/PyPlate
cd ~/Documents/Downloads/PyPlate-<version>$ ./install.sh
```

Next, cut/copy/paste the 'PyPlate' directory wherever you want. For the examples
below, we will use '~/Documents/Projects/Python/'.
```bash
foo@bar:~/Downloads$ mv PyPlate ~/Documents/Projects/Python
```

Lastly, you can delete the downloaded folder, if you copied it.

## Uninstalling
Just delete the 'PyPlate' folder from wherever you put it in the install step. 
PyPlate does not install anything on your system.

## Usage
PyPlate consists of two main scripts, 'pymaker.py' and 'pybaker.py'. The first
is used to create the project, and the second is used to update an existing
project as its development continues.

Let us start with 'pymaker.py'.

## PyMaker.py
Before you do anything, you should edit the 'user.json' file in 'PyPlate/conf'.
This file contains your personal information that is used when creating a new
project. These are one-time-only values and will not be updated automatically
later.  

The fields should be pretty self-explanatory, but here is a brief description of
each:

### PP_AUTHOR
The name to use for 'Author' in headers and pyproject.toml

### PP_DATE_FMT
The date format to use in headers

### PP_EMAIL
The email address to use in pyproject.toml

### PP_LICENSE
The license to use in headers

You may also want to edit the 'types.json' file in 'PyPlate/conf'. The default
file looks like this:
```
{
    "c": [
        "CLI",
        "CLIs",
        "cli"
    ],
    "g": [
        "GUI",
        "GUIs",
        "gui"
    ],
    "p": [
        "Package",
        "Packages",
        "pkg"
    ]
}
```
The structure of each entry looks like this:
```
{
    'short_type_name': {
        ['long_type_name', 'destination_folder', 'source_folder']
    }
}
```
where:

### short_type_name
A single letter (like 'c' for CLI projects)

### long_type_name
The name to display when asking for a project type (ie. 'CLI')

### destination_folder
The name of the folder under 'DIR_BASE' (explained below) to put the project in  

### source_folder
The folder under 'PyPlate/template' that the source files reside

This allows you to add/edit/delete project types, as well as their displayed
names and source\destination folders.

Next, to create a project, cd into the 'PyPlate/src' directory, and run
'pymaker.py':
``` bash
foo@bar:~$ cd ~/Documents/Projects/Python/PyPlate/src
foo@bar:~/Documents/Projects/Python/PyPlate/src$ ./pymaker.py
```

Enter the required information, and 'pymaker.py' will create the required files
and folders in a subdirectory of 'DIR_BASE', where 'DIR_BASE' is the directory
above 'PyPlate'. In our example, 'DIR_BASE' is '~/Documents/Projects/Python'.

So, from all of our assumptions above, if the project type is 'c', and the
project name is 'CLITest', then the project will be created in
'~/Documents/Projects/Python/CLIs/CLITest'.

That's it! From there you are free to modify the projects in your favorite IDE.

<hr>

## PyBaker.py / Updating the project
Once you have created a project, you can use 'pybaker.py' in the project's
'conf' directory to update metadata in the project's files.

'pybaker.py' is a script which will replace certain keywords in the project
directory. These keywords are placed in files in the 'conf' directory of your
project. These files are explained below.

The files in the 'conf' directory can be edited at any time (except
'settings.json'), followed by re-running 'pybaker.py'. The script uses regular
expressions to search for context (i.e. text before and after the replacement)
so as long as the context does not change, 'pybaker.py' can replace text at any
time. 

## Blacklist.json
You should edit this file by hand before running 'pybaker.py'. This file is used
by 'pybaker.py' to determine which files/folders it can (or rather, *can't*)
operate on.

Files in the new project are divided, internally, into four categories:
1. the file or directory's COMPLETE contents
2. the file's headers
3. the file's text (other than the header)
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
        "pybaker.py",
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
'pybaker.py' may fix the path, but not the internal contents of the file.

This is equivalent to placing the same file in both 'skip_header' and
'skip_text'.

This section is used for things like images, where the contents of the file are
not text, but you may want to fix the filename.

### skip_header
'pybaker.py' may fix the contents of the file, as well as the path, but not the
header contents.

This section is rarely used.

### skip_text
'pybaker.py' may fix the header, as well as the path, but not the other contents
of the file.

This section is commonly used for config files where the header should match the
project, but the contents should not be altered. 

*Note that 'skip_text' should ALWAYS include 'pybaker.py', 'settings.json', and
'strings.json', and should NEVER include 'blacklist.json'. This is because these
files have certain keywords which need to be replaced (or not replaced) in order
for 'pybaker.py' to function correctly.*

### skip_path
'pybaker.py' may fix the header, as well as the contents, but not the path of
the file.

This section is rarely used.

## Strings.json
You should edit this file by hand before running 'pybaker.py'. This file is used
by 'pybaker.py' to determine what strings should be replaced in the project.

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
This is the short description of the project, used in 'README.md' and
'pyproject.toml', as well as the GUI "About" dialog. Value is a string.

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
an array, with each value separated by a semicolon, and must end with a 
semicolon.  

Each entry must match an entry in the list found
[here](https://specifications.freedesktop.org/menu-spec/latest/apa.html).
If the entry does not match, it will be ignored, and an error will be printed.

## Settings.json

You should NOT edit this file by hand. It is created when PyPlate creates a new
project, and the dictionary is filled automatically. This file is used by
'pybaker.py' to get the initial project settings.

It is explained here only to show what it contains.

This the basic structure of 'settings.json':

```
{
    "project": {
        "type": "c"
    },
    "info": {
        "__PP_NAME_BIG__": "CLITest",
        "__PP_NAME_SMALL__": "clitest",
        "__PP_DATE__": "06/23/2023"
    }
}
```

And here is an explanation of what it contains:

## Project

### Type

Indicates the type of project: "c" for CLI, "g" for PyGObject GUI, or "p" for 
package.

## Info

### \_\_PP_NAME_BIG__

The properly capitalized name of the project, for use in strings displayed to
the user.

### \_\_PP_NAME_SMALL__

The lowercase version of the project name, used internally by pymaker.py and
pybaker.py.

### \_\_PP_DATE__

The date the project was created, used internally by pymaker.py and pybaker.py.

<hr>

After these files have been edited appropriately, run 'pybaker.py' from the
'conf' directory to update the metadata in the project. This module can be run
any time AFTER the project has been created to update the metadata in the
project. Here is an example for a project of type 'c' (CLI) named 'CLITest':

``` bash
foo@bar:~$ cd ~/Documents/Projects/Python/CLIs/CLITest/conf
foo@bar:~/Documents/Projects/Python/CLIs/CLITest/conf$ ./pybaker.py
```

'clitest.py' will print any errors it finds, along with the filename and line
number, so you can correct them.

## Notes
If you make any changes to this template to better suit your own style/setup,
please let me know or send a pull request. I will take a look and see if I can
incorporate your changes to make them user-agnostic. This way the template can
hopefully become more customizable to suit everyone's needs.

## -)
<!-- -) -->
