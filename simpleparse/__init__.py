"""
This makes making command line arguments a lot easier
"""

import argparse
import os
from os.path import join

from simpleparse import settings
from simplelog import log

import utils
import arguments

__version__ = "0.1"

SUBPARSERS = "SUBPARSERS"
PARSER = "PARSER"

_parser = None
_subparsers = None
_subcommands = None


### Utils

def find_commands(management_dir):
    """
    Given a path to a management directory, returns a list of all the command
    names that are available.

    Returns an empty list if no commands are defined.
    """
    command_dir = os.path.join(management_dir, 'commands')
    try:
        return [f[:-3] for f in os.listdir(command_dir)
                if not f.startswith('_') and f.endswith('.py')]
    except OSError:
        return []

### parser

def get_parser(**kwargs):
    """
    Get the default parser
    @param:
    kwargs - same args as argument parser
    """
    _parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            **_process_kwargs(kwargs)
            )
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
    #TODO: check for special args in kwargs
    _subparsers = parser.add_subparsers(**
            _process_kwargs(kwargs))
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


def setup_parser(*args, **kwargs):
    """
    Bootstrap Parser

    @param:
    parser - config parser
    subparser - config subparser
    subcommands - arguments for subparser
    funcs - dictionary of functions that subparsers will execute
    """
    log(args)
    kwargs_parser = kwargs.get('parser', {})
    kwargs_subparser = kwargs.get('subparser', {})
    arg_subcommand = kwargs.get('subcommands', [])
    kwargs_funcs = kwargs.get('funcs', {})

    if args:
        root = os.path.dirname(os.path.abspath(args[0]))
        _commands = find_commands(root)
        log(_commands)
        import imp
        #TODO: import module

    parser = get_parser(**kwargs_parser)
    subparser = get_subparser(parser, **kwargs_subparser)
    subcmds = get_subcommands(arg_subcommand)
    funcs = kwargs_funcs

    for cmd in subcmds.values():
        cmd_parser = subparser.add_parser(
                cmd["name"],
                **_process_kwargs(cmd)
                )
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
    #TODO: use _process_kwargs
    default = arg.get("default")
    if default is not None:
        default = utils.save_eval(default)
    utils.set_if_value_not_none(arg, 'default', default)

    parser.add_argument(*name, **arg)


def _process_kwargs(kwargs):
    """
    Sanitizes kwargs for add_parser
    """
    #TODO: better sanitization
    out = {}
    ignore = ["arguments", "name"]
    for k in kwargs.keys():
        v = kwargs[k]
        if k in ignore:
            continue
        else:
            out[k] = v
    return out


if __name__ == "__main__":
    parser = setup_parser()
