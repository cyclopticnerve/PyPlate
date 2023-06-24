<!----------------------------------------------------------------------------->
<!-- Project : PyPlate                                         /          \  -->
<!-- Filename: blacklist.md                                   |     ()     | -->
<!-- Date    : 12/19/2022                                     |            | -->
<!-- Author  : cyclopticnerve                                 |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

# Blacklist.json

You should edit this file by hand.

The default blacklist.json file will probably look something like this:
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
        "guitest.png"
    ],
    "skip_header": [],
    "skip_text": [
        "metadata.json",
        "metadata.py",
        "settings.json"
    ],
    "skip_path": []
}
```

The individual entries are:

## skip_all
A list of folders/files for which NOTHING should be done. Don't fix headers, 
text, or path. Leave them untouched. This section is usually used.

## skip_file
metadata.py may fix the path, but not the internal contents of the file. This 
section is commonly used.

## skip_header
metadata.py may fix the contents of the file, as well as the path, but not the 
header contents. This section is rarely used.

## skip_text
metadata.py may fix the header, as well as the path, but not the contents of 
the file. This section is commonly used for config files where the header 
should match the project, but the contents need to use variables from the other 
files.

## skip_path
metadata.py may fix the header, as well as the contents, but not the path of 
the file. This section is rarely used.

## -)
<!-- -) -->
