<!----------------------------------------------------------------------------->
<!-- Project : PyPlate                                         /          \  -->
<!-- Filename: settings.md                                    |     ()     | -->
<!-- Date    : 12/19/2022                                     |            | -->
<!-- Author  : cyclopticnerve                                 |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

# Settings.json

You should NOT edit this file by hand. It is created when PyPlate creates a new 
project, and the dictionary is filled automatically. This file is used by 
metadata.py to get the initial project settings.

This the basic structure of 'settings.json':

```
{
    "project": {
        "type": "m",
        "dir": "/home/<user>/Documents/Projects/Python/Libs/ModTest"
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

### Dir
 The full path to the project directory.

 ## Info

 ### \_\_PP_NAME_BIG__

 The properly capitalized name of the project, for use in strings displayed to 
 the user.

 ### \_\_PP_NAME_SMALL__

 The lowecase version of the project name, used internally by PyPlate and 
 metadata.py.

  ### \_\_PP_DATE__

  The date the project was created, used internally by PyPlate and metada.py.

## -)
<!-- -) -->
