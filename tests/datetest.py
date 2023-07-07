DEBUG = 'foo'

try:
    if DEBUG:
        print('true')
    else:
        print('false')
except (NameError):
    print('false')

"""
true    true
false   false
other   true
blank   false
none    false
"""
