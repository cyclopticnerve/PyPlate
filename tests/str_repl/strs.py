""" __PP_DIR_FOO__ """
'''__PP_DIR_FOO__'''

# pyplate: disable=replace
S1 = 'this # is'  # #  a test # comment "# more"" '
# bar#baz"not#or"#or#"this#"foo#bar# and " this #" '
S2 = "this is # a test" + " of foobar # "  # 'foobar' '# foobar'
# foobar: replace=enable
S3 = "pyplate: enable=replace"
X = 4
"""
# comment 
"""  # comment
'''
this is code
''' # foobar

# pyplate:enable=replace
""  # comment
X = "# pyplate: enable=replace" # pyplate: disable=replace
