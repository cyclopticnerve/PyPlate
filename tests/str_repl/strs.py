""" __PP_DIR_FOO__ """

S1 = "This is a test"
S2 = "__PP_DIR_FOO__"
S3 = "Test inline" # __PP_DIR_FOO__

# __PP_DIR_FOO__

def func():
    """
    don't replace this
    __PP_DIR_FOO__
    """

S4 = "do this __PP_DIR_FOO__"
