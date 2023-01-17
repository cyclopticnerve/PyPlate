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

A template for creating packages/modules/CLI apps/GTK3 apps in Python

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
from the main branch.

Download either the 'tar.gz' or '.zip' file and extract it.

Or you can clone the git repo to get the latest (and often broken) code 
from the dev branch:

```bash
foo@bar:~$ cd Downloads
foo@bar:~/Downloads$ git clone https://github.com/cyclopticnerve/PyPlate
```

Next, cut/copy/paste/cp/mv the PyPlate directory wherever you want. For all 
examples below, we will use "~/Documents/Projects/Python/".
```bash
foo@bar:~/Downloads$ cp PyPlate ~/Documents/Projects/Python
```

Lastly, you can delete the downloaded folder.

## Uninstalling

Just delete the PyPlate folder from wherever you put it in the install step.

## Usage

You may want to edit the the PyPlate/src/pymaker.json file before first run. 
This file contains settings to determine where new projects will be placed.

| Key       | Value                                                           | Default                  |
| --------- | --------------------------------------------------------------- | ------------------------ |
| conf_base | The base directory for creating new projects                    | the folder above PyPlate |
| conf_libs | The subdirectory below prj_base for Module and Package projects | ''                       |
| conf_apps | The subdirectory below prj_base for CLI and GUI app projects    | ''                       |
| conf_date | The date format to use in file headers (in strftime format)     | %Y-%m-%d                 |
| conf_auth | The author's (your) name for headers and other config files     | os.getlogin()            |
| conf_mail | The author's (your) email for config files                      | ''                       |
| conf_lcns | The name of the license to use in the header (not actual file)  | ''                       |

If conf_libs or conf_apps is empty, projects will be created in conf_base.

For more on the date_fmt and strftime() function, see [this page](https://strftime.org/).
You can also put blank entries for any of the values, in which case they will 
revert to thier defaults.

Next, cd into the PyPlate/src folder, then run pymaker.py:

``` bash
foo@bar:~$ cd Documents/Projects/Python/PyPlate/src
foo@bar:~/Documents/Projects/Python/PyPlate/src$ ./pymaker.py
```

Enter the required information, and pymaker.py will create the required files 
and folders in a subdirectory of conf_base/conf_libs or conf_base/conf_apps 
based on your entries.

From there you are free to modify the projects in your favorite IDE.

## Notes

## -)
<!-- -) -->
