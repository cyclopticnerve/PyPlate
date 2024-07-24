"""doc"""

# TODO: will this fix header lines? it should, since we scan for them by regex
# and fix separately from code

from pathlib import Path

path = Path(__file__).parent.resolve()
path = path / "strs.py"

IN_TRIPS = False

def fix():
    """doc"""

    print()

    with open(path, "r", encoding="UTF8") as a_file:
        lines = a_file.readlines()

    global IN_TRIPS
    IN_TRIPS = False

    for index, line in enumerate(lines):
        # lines = lines_fix(lines)
        # print(lines)
        lines[index] = lines_fix(line)

    print(lines)


def lines_fix(line):
    """doc"""

    # skip blank lines
    if line.strip() == "" or line.strip().startswith("#"):
        return line

    # --------------------------------------------------------------------------

    # skip trips lines/trips blocks
    global IN_TRIPS

    # find trips
    a_count = line.count('"""')

    # we found a trip
    if a_count > 0:

        # if it is a one-liner
        if a_count > 1:

            # single line trips, just skip
            IN_TRIPS = False
            return line

        # flip in_trips flag and skip
        IN_TRIPS = not IN_TRIPS
        return line

    # skip trips and their contents
    if IN_TRIPS:
        return line

    # --------------------------------------------------------------------------

    # ignore trailing comments
    parts = line.split("#")

    # replace content
    parts[0] = parts[0].replace("__PP_DIR_FOO__", "a_dir")

    # rejoin trailing comments
    line = "#".join(parts)

    return line


# ------------------------------------------------------------------------------

# do the thing
if __name__ == "__main__":
    fix()
