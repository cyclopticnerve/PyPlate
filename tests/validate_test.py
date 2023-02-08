import re

"""
this works for 1 & 2 char
(^[a-zA-Z])([a-zA-Z\d]*$)

if only group 1, ok
if group 1 and group 3, ok

"""

# pattern = r'( ^ [a-zA-Z0-9_\-]*)'

# while True:
#     name = input('name:')

#     matches = re.finditer(pattern, name, re.MULTILINE)

#     for matchNum, match in enumerate(matches, start=1):

#         print("Match {matchNum} found at {start}-{end}: {match}".format(
#             matchNum=matchNum, start=match.start(), end=match.end(),
#             match=match.group()))

#         print(len(match.groups()))
#         for groupNum in range(0, len(match.groups())):
#             groupNum = groupNum + 1

#             print("Group {groupNum} found at {start}-{end}: {group}".format(
#                 groupNum=groupNum, start=match.start(groupNum),
#                 end=match.end(groupNum), group=match.group(groupNum)))

while True:

    name = input('name:')

    # create match pattern strings
    pattern_start = r'(^[a-zA-Z])'
    pattern_end = r'([a-zA-Z0-9]$)'
    pattern_middle = r'(^[a-zA-Z0-9\-]*$)'

    # match start or return false
    search_start = re.search(pattern_start, name)
    if not search_start:
        print('Project names must start with a letter')
        continue

    # match end or return false
    search_end = re.search(pattern_end, name)
    if not search_end:
        print('Project names must end with a letter or number')
        continue

    # match middle or return false
    search_middle = re.search(pattern_middle, name)
    if not search_middle:
        print('Project names must contain only letters, numbers, hyphens (-),'
              ' underscores (_), and spaces')
        continue

    # if we made it this far, return true
    print('ok')
    continue
