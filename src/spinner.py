# ------------------------------------------------------------------------------
# Package :PyPlate                                                /          \
# Filename: spinner.py                                            |     ()     |
# Date    : 09/04/2026                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# TODO: ctrl-c still wonky
"""
A decorator to print a spinner in a status line
Heavily inspired by Dave Eddy (https://www.youtube.com/@yousuckatprogramming)

For decorator templates, see cndecorator.py and cndecorator_params.py in this
directory.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import signal
from threading import Thread, Event
from time import sleep
from typing import Callable

# lib imports
from cnlib import cnfunctions as F

# local imports
import conf

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Strings


# ------------------------------------------------------------------------------
# Dictionaries

# default spinner options

# frames:   List of strings to rotate through when animating the spinner
# interval: Amount of time, in seconds, between animation frames (accepts
#           fractional time)
# skip:     Dict of stuff to print when skipped
# done:     Dict of stuff to print when done
# fail:     Dict of stuff to print when failed

# result:   What to print after msg
# fg:       Foreground color for pass/fail

# conf.D_SPIN = {
#     # S_KEY_FRAMES: ["", ".", "..", "..."],
#     # S_KEY_INTERVAL: 0.5,
#     # S_KEY_SKIP: {
#     #     S_KEY_RES: "Skipped",
#     #     S_KEY_FG: F.C_FG_YELLOW
#     # },
#     # S_KEY_DONE: {
#     #     S_KEY_RES: "Done",
#     #     S_KEY_FG: F.C_FG_GREEN
#     # },
#     # S_KEY_FAIL: {
#     #     S_KEY_RES: "Failed",
#     #     S_KEY_FG: F.C_FG_RED
#     # },
# }


class SpinnerError(Exception):
    """docstring"""

    # pass


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Trap SIGINT (Ctrl-C) to restore cursor
# ------------------------------------------------------------------------------
def _signal_handler(_sig, _frame):
    """
    Trap SIGINT (Ctrl-C) to restore cursor
    """

    # restore cursor
    print(conf.S_SHOW_CURSOR, end="")

    # raise an error that says ctrl-c was pressed
    raise SpinnerError(conf.S_ERR_CTRL_C)


# ------------------------------------------------------------------------------
# The code to draw the spinner on a background thread
# ------------------------------------------------------------------------------
def _thread_spin(evt: Event, msg: str):
    """
    The code to draw the spinner on a background thread

    Arguments:
        evt: Event object to control stopping the thread
        msg: Tell the user what is happening

    This is a private function that handles the animation of the line.
    """

    # get animation frames and interval between frames from local dict
    frames = conf.D_SPIN[conf.S_KEY_FRAMES]
    interval = conf.D_SPIN[conf.S_KEY_INTERVAL]

    # hide cursor, cursor stays
    print(conf.S_HIDE_CURSOR, end="")

    # start spinner and run until flag
    while not evt.is_set():

        # for each frame of animation
        for frame in frames:

            # clear current line, cursor stays
            print(conf.S_CLEAR_LINE, end="")

            # print msg and frame, cursor to line start
            # NB: the \r is here because S_CLEAR_LINE clears to the right of
            # the cursor
            a_str = conf.S_MSG_FMT.format(msg, frame)
            print(a_str, end="\r")

            # wait for interval
            sleep(interval)

    # show cursor, cursor stays
    print(conf.S_SHOW_CURSOR, end="")


# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Print the skip message
# ------------------------------------------------------------------------------
def skip(msg: str):
    """
    Print the skip message

    Arguments:
        msg: Step name to print
    """

    # get last frame
    frames = conf.D_SPIN[conf.S_KEY_FRAMES]
    frame = frames[-1]

    # print message and last frame
    a_str = conf.S_MSG_FMT.format(msg, frame)
    print(a_str, end="")

    # print yellow skip
    a_dict = conf.D_SPIN[conf.S_KEY_SKIP]
    F.printc(
        a_dict[conf.S_KEY_RES],
        fg=a_dict[conf.S_KEY_FG],
        bold=True,
    )


# ------------------------------------------------------------------------------
# Decoration implementation with params
# ------------------------------------------------------------------------------
def spin(msg: str) -> Callable:
    """
    Decoration implementation with params

    Arguments:
        msg: The string to use as the message

    Returns:
        The function that matches <some_name>(some_func), which in turn returns
        wrapper(*args, ** kwargs), which is called instead of the decorated
        function

    This function is the main entry point for the decorator, passing the
    function signature and parameters as they are called in code, as a hidden
    first param. It also passes the parameters passed to the decorator.
    """

    # --------------------------------------------------------------------------
    # Decoration implementation with no parameters
    # --------------------------------------------------------------------------
    def spin2(func: Callable) -> Callable:
        """
        Decoration implementation with no parameters

        Arguments:
            func: The object representation of the function to be decorated
            (name, params/types, return type)

        Returns:
            The function that matches wrapper(*args, ** kwargs), which is
            called instead of the decorated function

        Do some stuff before and after calling the original function.
        """

        # ----------------------------------------------------------------------
        # The one that does all the work
        # ----------------------------------------------------------------------
        def wrapper(*args, **kwargs):
            """
            The one that does all the work

            Arguments:
                *args: List of all args that do not have keywords (positional
                args)
                **kwargs: Dict of all args that do have keywords (foo=bar,
                etc.)

            This method does the real work, performing the before-call code,
            the actual function, and the after-call code.
            """

            # create thread outside of try so we can get it in except
            evt = Event()
            t_spin = Thread(target=_thread_spin, args=(evt, msg))

            # start spinner on new thread
            t_spin.start()

            # store error if raised
            err = None

            # ------------------------------------------------------------------
            # ------------------------------------------------------------------

            # try to run the real function and see if it passes/fails
            # yes, or no and why
            try:
                func(*args, **kwargs)

            # catch ALL exceptions to print fail and restore cursor
            # NB: we are not interested in handling the error here, we just
            # need to know IF it happened
            # we will re-raise it to let the real function handle it
            except Exception as e:  # pylint: disable=broad-exception-caught
                err = e

            # ------------------------------------------------------------------
            # ------------------------------------------------------------------

            # do these regardless of result

            # stop animation thread
            evt.set()
            t_spin.join()

            # get last frame
            frames = conf.D_SPIN[conf.S_KEY_FRAMES]
            frame = frames[-1]

            # print message and last frame
            a_str = conf.S_MSG_FMT.format(msg, frame)
            print(a_str, end="")

            # ------------------------------------------------------------------
            # do these based on result

            # only thing that fails is explicit False or error
            # if res is False or isinstance(res, Exception):
            if err:

                # print red fail
                a_dict = conf.D_SPIN[conf.S_KEY_FAIL]
                F.printc(
                    a_dict[conf.S_KEY_RES],
                    fg=a_dict[conf.S_KEY_FG],
                    bold=True,
                )
                # print error if F.B_DEBUG is True
                F.printd(str(err))
            else:

                # print green done
                a_dict = conf.D_SPIN[conf.S_KEY_DONE]
                F.printc(
                    a_dict[conf.S_KEY_RES],
                    fg=a_dict[conf.S_KEY_FG],
                    bold=True,
                )

            # TODO: raising an error here would get the last fail to print
            # and also get the program to halt (fail on first error)

            if isinstance(err, SpinnerError):  # as c_error:

                # restore cursor
                print(conf.S_SHOW_CURSOR, end="")

                # send error up to caller
                raise err

            # return None (pass) or Exception (fail)
            return err

        # restore cursor
        print(conf.S_SHOW_CURSOR, end="")

        # return wrap func as new pointer for a_func
        # NB: this is the function that ultimately gets called
        return wrapper

    # restore cursor
    print(conf.S_SHOW_CURSOR, end="")

    # return inner here
    return spin2


# any interrupt calls above handler
signal.signal(signal.SIGINT, _signal_handler)


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    F.B_DEBUG = True

    # --------------------------------------------------------------------------

    @spin("Real downloading file")
    def do_long():
        """docstring"""

        # sleep(10)  # do something

        # try:
        # F.run("ls", shell=True)
        # F.run("boogers")
        # except F.CNRunError as e:
        #     # NB: re-raise error so wrapper knows it failed
        #     raise e

        # raise OSError("error: boobs")

    # --------------------------------------------------------------------------

    # do the thing
    skip("Skip downloading file")
    ERR = do_long()
    if ERR:
        print("oops")
    else:
        print("ok")
    # print("goodbye")

# -)
