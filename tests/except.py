"""
docstring
"""

import shlex
import subprocess


class CNShellError(Exception):
    """
    docstring
    """

    def __init__(self, exception):
        self.exception = exception
        self.__repr__ = self.exception.__repr__


# ------------------------------------------------------------------------------
# Run a command string in the shell
# ------------------------------------------------------------------------------
def sh(cmd, shell=False):
    """
    Run a command string in the shell

    Arguments:
        cmd: The command line to run
        shell: If False (the default), run the cmd as one long string. If True,
        split the cmd into separate arguments

    Raises:
        Exception if something went wrong

    Returns:
        The result of running the command line, as a
        subprocess.CompletedProcess object

    This is just a dumb convenience method to use subprocess with a string
    instead of having to convert a string to an array with shlex every time I
    need to run a shell command.
    """

    # make sure it's a string (sometime pass path object)
    cmd = str(cmd)

    # split the string using shell syntax (smart split/quote)
    # NB: only split if running a file - if running a shell cmd, don't split
    if not shell:
        cmd = shlex.split(cmd)

    # get result of running the shell command or bubble up an error
    try:
        res = subprocess.run(
            # the array of commands produced by shlex.split
            cmd,
            # if check is True, an exception will be raised if the return code
            # is not 0
            # if check is False, no exception is raised but res will be None,
            # meaning you have to test for it in the calling function
            # but that also means you have no information on WHY it failed
            check=True,
            # convert stdout/stderr from bytes to text
            text=True,
            # put stdout/stderr into res
            capture_output=True,
            # whether the call is a file w/ params (False) or a direct shell
            # input (True)
            shell=shell,
        )
    except Exception as e:
        # bubble up the error to the calling function
        new_err = CNShellError(e)
        raise new_err from e

    # return the result
    return res

try:
    CMD2 = "echo 'HELLO'"
    res2 = sh(CMD2, shell=False)
    print(res2.stdout)
except CNShellError as e:
    print(e)
