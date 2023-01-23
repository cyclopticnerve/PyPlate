# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pyheaders.py                                          |     ()     |
# Date    : 1/17/2023                                             |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# NB: this code moved to its own file until i can figure out a better way to do
# headers - ie user-agnostic, maybe as a rep... see misc/parshdr.py

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Function for replacing header text inside files
# ------------------------------------------------------------------------------
def replace_headers(lines, reps):

    """
        Function for replacing header text inside files

        Paramaters:
            lines [list]: the file contents as a list of lines
            reps [list]: the list of replacements to use inside the headers

        Returns:
            [list]: the new list of lines representing the file

        This is a function to replace header text inside a file. Given a list of
        file lines and a list of replacement strings, it iterates the file line
        by line, replacing header text as it goes. When it is done, it saves the
        file to disk. This replaces the __CN_.. stuff inside headers.
    """

    # an array that represents the three sections of a header line
    hdr_lines = [
        ['# Project : ', '__CN_BIG_NAME__',   '/          \\ '],
        ['# Filename: ', '__CN_SMALL_NAME__', '|     ()     |'],
        ['# Date    : ', '__CN_DATE__',       '|            |'],
        ['# Author  : ', '__CN_AUTHOR__',     '|   \\____/   |'],
        ['# License : ', '__CN_LICENSE__',    ' \\          / '],
        ['<!-- Project : ', '__CN_BIG_NAME__',   '/          \\  -->'],
        ['<!-- Filename: ', '__CN_SMALL_NAME__', '|     ()     | -->'],
        ['<!-- Date    : ', '__CN_DATE__',       '|            | -->'],
        ['<!-- Author  : ', '__CN_AUTHOR__',     '|   \\____/   | -->'],
        ['<!-- License : ', '__CN_LICENSE__',    ' \\          /  -->'],
    ]

    # open file as text line array
    # with open(path) as file:
    #     lines = file.readlines()

    # for each line in array
    for i in range(0, len(lines)):

        # for each repl line
        for hdr_line in hdr_lines:

            # build start str
            key = hdr_line[0] + hdr_line[1]

            # if the key is in the line
            if key in lines[i]:

                # replace the dunder
                rep = reps[hdr_line[1]]

                # calculate spaces
                spaces = 80 - (len(hdr_line[0]) + len(rep) + len(hdr_line[2]))
                spaces_str = ' ' * spaces

                # create replacement string (with newline!!!)
                rep_str = f'{hdr_line[0]}{rep}{spaces_str}{hdr_line[2]}\n'

                # replace text in line
                lines[i] = rep_str

    # return file contents with header replacements
    return lines

# -)
