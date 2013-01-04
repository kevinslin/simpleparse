"""
This makes making command line arguments a lot easier
"""

import argparse

from simpleparse import settings
import utils
import arguments

SUBPARSERS = "SUBPARSERS"
PARSER = "PARSER"

_parser = None
_subparsers = None
_subcommands = None


def get_parser(**kwargs):
    """
    Get the default parser
    @param:
    kwargs - same args as argument parser
    """
    _parser = argparse.ArgumentParser(
        #TODO: do this properly
        description=kwargs.get("description", settings.DESCRIPTION_PARSER),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args = kwargs.get('arguments', {})
    for arg in args:
        _add_argument(_parser, arg)
    return _parser


def get_subparser(parser, **kwargs):
    """
    Get default subparser
    @param:
    help - help string
    """
    _subparsers = parser.add_subparsers(
        help=kwargs.get("help", settings.HELP_SUBPARSER))
    return _subparsers


def get_subcommands(subcmds):
    """
    Return dictionary mapping subcmd to args
    @param:
    subcmds - list of subcommands
    """
    _subcommands = {}
    if (subcmds is None):
        subcmds = []
    for arg in subcmds:
        _subcommands[arg['name']] = arg
    return _subcommands


def setup_parser(**kwargs):
    """
    Bootstrap Parser

    @param:
    parser - config parser
    subparser - config subparser
    subcommands - arguments for subparser
    funcs - dictionary of functions that subparsers will execute
    """
    kwargs_parser = kwargs.get('parser', {})
    kwargs_subparser = kwargs.get('subparser', {})
    arg_subcommand = kwargs.get('subcommands', [])
    kwargs_funcs = kwargs.get('funcs', {})

    parser = get_parser(**kwargs_parser)
    subparser = get_subparser(parser, **kwargs_subparser)
    subcmds = get_subcommands(arg_subcommand)
    funcs = kwargs_funcs

    for cmd in subcmds.values():
        cmd_parser = subparser.add_parser(cmd["name"])
        cmd_parser.set_defaults(fun=funcs[cmd["name"]])

        for arg in cmd.get("arguments", []):
            _add_argument(cmd_parser, arg)

    return parser

def _add_argument(parser, arg):
    """
    Translate arguments into params for add_argument
    and add to parser
    @param:
    arg - dictionary of key value pairs for argument
    """
    name = arg.pop('name')
    if isinstance(name, list) is False:
        name = [name]
    # special values
    #TODO: type, and other special values
    default = arg.get("default")
    if default is not None:
        default = utils.save_eval(default)
    utils.set_if_value_not_none(arg, 'default', default)

    parser.add_argument(*name, **arg)



if __name__ == "__main__":
    parser = setup_parser()
