# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: pp_argparse.py                                        |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import argparse

'''
https://docs.python.org/3/library/argparse.html#help

add_argument
    name or flags: 'pos' | '-o,--opt' | '-o', '--opt'
    action: (only used for opt args?)
        'store' (default action)
        'store_const' (needs 'const=' param, val=const if key present)
        'store_true'/'store_false' (stores action if key is present, !action if not)
        'append' (one value per key appearance, appends after 'default=')
        'append_const' (need 'dest=', 'const=' params, collates store_const into dest list)
        'count' (needs 'default=0', else default=None, counts number of param appearnces [-vvv])
        'help' (built-in, see below)
        'version' (needs 'version=')
        'extend' ('nargs=', 'type=', this seems to flatten differnt lists)
    nargs:
        'N' (=1 == ['a'], default == 'a')
        '?' for pos, use arg or def (zero or one)
          for opt, if opt present, use arg or const, else use def
        '*' gather all values unto me (zero or more)(also '?' rules apply)
        '+' like '*', but one or more (error if not at least one)
    const
        value to store when arg has no value or nargs=?
    default
        value to use for arg if value not present (see also narg rules)
        can also be suppressed by 'default=argparse.SUPPRESS'
    type
        convert strings passed in the commnad line to other types
    choices
        restrict entries to ['one', 'two', 'three'] | range(1-4)
    required
        makes -/-- options required. DON'T DO THIS
    help
        show help for argument
        add any params as:
        %(name)s
        %(action)s
        %(nargs)s
        %(const)s
        %(default)s
        %(type)s
        %(choices)s
        %(required)s
        %(metavar)s
        %(dest)s
    metavar
        changes display name of optional val or positional name in help
    dest
        instead of storing a value in the arg key, store it in a custom key
'''

"""
{
    '_action_groups': [
        <argparse._ArgumentGroup object at 0x7f5894d8f220>,
        <argparse._ArgumentGroup object at 0x7f5894d8d5d0>
    ],
    '_actions': [
        _HelpAction(
            option_strings=[
                '-h', '--help'
            ],
            dest='help',
            nargs=0,
            const=None,
            default='==SUPPRESS==',
            type=None,
            choices=None,
            required=False,
            help='show this help message and exit',
            metavar=None
        ),
        _VersionAction(
            option_strings=[
                '-v', '--version'
            ],
            dest='version',
            nargs=0,
            const=None,
            default='==SUPPRESS==',
            type=None,
            choices=None,
            required=False,
            help='Shows the version number for this program',
            metavar=None
        ),
        _StoreAction(
            option_strings=[
                '--bar'
            ],
            dest='bar',
            nargs=None,
            const=None,
            default=None,
            type=None,
            choices=None,
            equired=False,
            help=None,
            metavar=None
        )
    ],
    '_defaults': {},
    '_has_negative_number_optionals': [],
    '_mutually_exclusive_groups': [],
    '_negative_number_matcher': re.compile(
        '^-\\d+$|^-\\d*\\.\\d+$'
    ),
    '_option_string_actions': {
        '--bar': _StoreAction(
            option_strings=[
                '--bar'
            ],
            dest='bar',
            nargs=None,
            const=None,
            default=None,
            type=None,
            choices=None,
            required=False,
            help=None,
            metavar=None
        ),
        '--help': _HelpAction(
            option_strings=[
                '-h', '--help'
            ],
            dest='help',
            nargs=0,
            const=None,
            default='==SUPPRESS==',
            type=None,
            choices=None,
            required=False,
            help='show this help message and exit',
            metavar=None
        ),
        '--version': _VersionAction(
            option_strings=[
                '-v', '--version'
            ],
            dest='version',
            nargs=0,
            const=None,
            default='==SUPPRESS==',
            type=None,
            choices=None,
            required=False,
            help='Shows the version number for this program',
            metavar=None
        ),
        '-h': _HelpAction(
            option_strings=[
                '-h', '--help'
            ],
            dest='help',
            nargs=0,
            const=None,
            default='==SUPPRESS==',
            type=None,
            choices=None,
            required=False,
            help='show this help message and exit',
            metavar=None
        ),
        '-v': _VersionAction(
            option_strings=[
                '-v', '--version'
            ],
            dest='version',
            nargs=0,
            const=None,
            default='==SUPPRESS==',
            type=None,
            choices=None,
            required=False,
            help='Shows the version number for this program',
            metavar=None
        )
    },
    '_optionals': <argparse._ArgumentGroup object at 0x7f5894d8d5d0>,
    '_positionals': <argparse._ArgumentGroup object at 0x7f5894d8f220>,
    '_registries': {
        'action': {
            None: <class 'argparse._StoreAction'>,
            'append': <class 'argparse._AppendAction'>,
            'append_const': <class 'argparse._AppendConstAction'>,
            'count': <class 'argparse._CountAction'>,
            'extend': <class 'argparse._ExtendAction'>,
            'help': <class 'argparse._HelpAction'>,
            'parsers': <class 'argparse._SubParsersAction'>,
            'store': <class 'argparse._StoreAction'>,
            'store_const': <class 'argparse._StoreConstAction'>,
            'store_false': <class 'argparse._StoreFalseAction'>,
            'store_true': <class 'argparse._StoreTrueAction'>,
            'version': <class 'argparse._VersionAction'>
        },
        'type': {
            None: <function ArgumentParser.__init__.<locals>.identity at 0x7f58956cbd90>
        }
    },
    '_subparsers': None,
    'add_help': True,
    'allow_abbrev': True,
    'argument_default': None,
    'conflict_handler': 'error',
    'description': 'PP_SHORT_DESC',
    'epilog': None,
    'exit_on_error': True,
    'formatter_class': <class 'argparse.HelpFormatter'>,
    'fromfile_prefix_chars': None,
    'prefix_chars': '-',
    'prog': 'test.py',
    'usage': None
}
"""


def main():
    args = parse_args()
    print('-----')
    print(args)
    print('-----')
    print('foo')


def parse_args():
    """
        The main function of the module

        Returns:
            [list]: The Namespace object for argaprse (which seems to be a dict?
            of key=name)

        This function is the main entry point for the module, initializing the
        module, and performing it's steps.
    """

    # always print prog name/version
    print('__PP_NAME_BIG__ version PP_VERSION')

    # create the pasrser
    parser = argparse.ArgumentParser(
        description='PP_SHORT_DESC'
    )

    # add default cmd-line args
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='PP_VERSION'
    )

    # isolate the code to add args
    _add_args(parser)

    # # parse the cmd-line args
    args = parser.parse_args()

    # convert args to dict
    ret_args = vars(args)

    # if no args, print usage
    if len(ret_args) == 0:
        parser.print_usage()

    # return the parsed args
    return ret_args


def _add_args(parser):

    parser.add_argument('--bar')
    return


if __name__ == '__main__':
    main()

# -)
