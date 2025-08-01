"""file docstring"""

def dialog(message, buttons, default="", btn_sep="/", msg_fmt="{} [{}]: "):
    """method docstring"""

    # make all params lowercase
    buttons = [item.lower() for item in buttons]
    default = default.lower()

    # --------------------------------------------------------------------------

    # if we passes a default
    if default != "":

        # find the default
        if not default in buttons:

            # not found, add at end of buttons
            buttons.append(default)

        # upper case it
        buttons[buttons.index(default)] = default.upper()

    # --------------------------------------------------------------------------

    # add buttons to message
    btns_all = btn_sep.join(buttons)
    str_fmt = msg_fmt.format(message, btns_all)

    # lower everything again for compare
    buttons = [item.lower() for item in buttons]

    # --------------------------------------------------------------------------

    while True:

        # ask the question, get the result
        inp = input(str_fmt)
        inp = inp.lower()

        # ----------------------------------------------------------------------

        # # no input (empty)
        if inp == "" and default != "":
            return default

        # input a button
        if inp in buttons:
            return inp

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# while True:
res = dialog("test dialog", ["y", "n"], "X")
print(res)
