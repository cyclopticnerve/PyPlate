"""
    docstring
"""

# NB: see also google doc

# img: https://img.shields.io/badge/License-WTFPL-brightgreen.svg
# url: http://www.wtfpl.net

G_STR_LICENSE_ALT = "License"
G_STR_LICENSE_NONE = "None"

# get replacement value
pp_license_name = ""
pp_license_img = "https://img.shields.io/badge/License-WTFPL-brightgreen.svg"
pp_license_url = "http://www.wtfpl.net"

# we have no name
if pp_license_name == "":
    # 0 x x
    if pp_license_img == "":
        # 0 0 x
        if pp_license_url == "":
            # 0 0 0
            pp_license_full = f"{G_STR_LICENSE_ALT}: {G_STR_LICENSE_NONE}"
        else:
            # 0 0 1
            pp_license_full = (
                f'[{G_STR_LICENSE_ALT}]({pp_license_url} "{pp_license_url}")'
            )
    else:
        # 0 1 x
        if pp_license_url == "":
            # 0 1 0
            pp_license_full = f"![{G_STR_LICENSE_ALT}]({pp_license_img})"
        else:
            # 0 1 1
            pp_license_full = (
                f'[![{G_STR_LICENSE_ALT}]({pp_license_img} "{pp_license_url}")]'
                f"({pp_license_url})"
            )

with open("tests/license_test.md", "w", encoding="UTF-8") as a_file:
    a_file.write(pp_license_full)

print(pp_license_full)
