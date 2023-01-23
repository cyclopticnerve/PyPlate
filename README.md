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

A template for creating modules/packages/CLI apps/GTK3 apps in Python

## Requirements
None

## Installing
You should first run:
```bash
foo@bar:~$ sudo apt update && sudo apt upgrade
```
to make sure you have the lastest software installed.

You can download the (hopefully stable)
[latest release](https://github.com/cyclopticnerve/PyPlate/releases/latest) 
from the main branch.<br>
Download either the 'tar.gz' or '.zip' file and extract it.

Or you can clone the git repo to get the latest (and often broken) code 
from the dev branch:
```bash
foo@bar:~$ cd Downloads
foo@bar:~/Downloads$ git clone https://github.com/cyclopticnerve/PyPlate
```
Next, cut/copy/paste/cp/mv the 'PyPlate' directory wherever you want. For all 
examples below, we will use '~/Documents/Projects/Python/'.
```bash
foo@bar:~/Downloads$ cp PyPlate ~/Documents/Projects/Python
```

Lastly, you can delete the downloaded folder, if you copied it.

## Uninstalling
Just delete the 'PyPlate' folder from wherever you put it in the install step.

## Usage
To create a project, cd into the 'PyPlate/src/' directory, and run 'pymaker.py':
``` bash
foo@bar:~$ cd Documents/Projects/Python/PyPlate/src
foo@bar:~/Documents/Projects/Python/PyPlate/src$ ./pymaker.py
```

The first time you run 'PyPlate/src/pymaker.py', it will generate a default 
'pymaker.json' file in the 'PyPlate/src/' directory, show a message, and exit. 
You will definitely want to edit the 'pymaker.json' file before the next run. 
This file contains settings which determine where and how new projects are 
created. If you don't edit it, you will end up with a lot of empty replacements 
that are hard to format/replace by hand. 

| Key       | Value                                                     | Default               |
| --------- | --------------------------------------------------------- | --------------------- |
| conf_base | Base directory for creating new projects                  | Folder above PyPlate  |
| conf_mods | Subdirectory below conf_base for Module projects          | ''                    |
| conf_pkgs | Subdirectory below conf_base for Package projects         | ''                    |
| conf_clis | Subdirectory below conf_base for CLI app projects         | ''                    |
| conf_guis | Subdirectory below conf_base for GUI app projects         | ''                    |
| conf_date | Date format to use in file headers (in strftime() format) | locale formatted date |
| conf_auth | Author's (your) name for headers and other config files   | ''                    |
| conf_mail | Author's (your) email for config files                    | ''                    |
| conf_lcns | Name of the license to use in headers (not actual file)   | ''                    |

If any of the subdirectory entries are blank, projects will be created in 
'conf_base', without a subdirectory.<br>
If any other entries are blank, they will revert to their defaults (where 
applicable).

For more on the 'conf_date' value and *strftime()* function, see 
[this page](https://strftime.org/). The easiest here is to leave it blank, since 
it will then be formatted using your locale. (mm/dd/yy for US, or dd/mm/yy for 
EU, etc.)

After the first run and editing 'pymaker.json', run 'pymaker.py' again.

Enter the required information, and 'pymaker.py' will create the required files 
and folders in a subdirectory of 'conf_base/conf_libs', etc. based on your 
entries.

From there you are free to modify the projects in your favorite IDE.

## Notes

I couldn't find an easy way to include an empty (or default) 'pymaker.json' file 
in the GitHub repo, while still maintaining my own 'pymaker.json' file that 
works on my system. That's why you have to run 'pymaker.py' once to create a 
default file, then edit it. This project is meant to be drag-and-drop, and as 
such there is no code that runs at install, so no file-wrangling is done before 
the first run. Sorry if this causes confusion.

A simple solution to this would be to have a seperate file or function that
detects a 'first run', and walks the user through setting each value in the key
list, then runs the actual 'pymaker.py' using the new conf file. Not interested
in this ATM, but maybe soon?

I've tried to make this template as user-agnostic as possible, while still being
useful for me. As such, some files/folders may not be useful to you, or you may
need other files/folders not included in this template. I am working on making
the file/folder structure more user-definable, as well as things like headers
and footers, comment styles, etc. but I can only base it on my own style. So...

If you make any changes to this template to better suit your own style/setup, 
please let me know or send a pull request. I will take a look and see if I can 
incorporate your changes to make them user-agnostic. This way the template can 
hopefully become more customizable to suit everyone's needs.

## -)
<!-- -) -->
