"""
This makes making command line arguments a lot easier
"""

import argparse

from simpleparse import settings
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
    description - description of arg parser
    """
    global _parser

    if _parser is None:
        _parser = argparse.ArgumentParser(
            description=kwargs.get("description", settings.DESCRIPTION_PARSER),
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    return _parser


def get_subparser(**kwargs):
    """
    Get default subparser
    @param:
    help - help string
    """
    global _parser, _subparsers

    if _parser is None:
        _parser = get_parser()

    _subparsers = _parser.add_subparsers(
        help=kwargs.get("help", settings.HELP_SUBPARSER))
    return _subparsers


def get_subcommands(**kwargs):
    """
    Get all subcommands
    @param:
    subparsers - dictionary to configure subparsers
    """
    global _subcommands

    if _subcommands is None:
        _subcommands = {}
        for arg in kwargs.get("subparsers", arguments.SUBPARSERS):
            _subcommands[arg['name']] = arg
    return _subcommands


def setup_parser(**kwargs):
    """
    Bootstrap Parser

    @param:
    parser
    subparsers
    commands - dictionary of functions
    """
    #TODO: parser and subparser might share same kwargs
    parser = get_parser(**kwargs)
    subparser = get_subparser(**kwargs)
    cmds = get_subcommands(**kwargs)
    commands = kwargs.get("commands", {})
    for cmd in cmds.values():
        cmd_parser = subparser.add_parser(cmd["name"])
        cmd_parser.set_defaults(fun=commands[cmd["name"]])

        for arg in cmd.get("arguments", []):
            name = arg["name"]
            if (type(name) is type("")):
                name = [name]
            default = arg.get("default")
            if default is not None:
                default = eval(default)
            cmd_parser.add_argument(*name,
                    help = arg.get("help"),
                    default = default,
                    action = arg.get("action"))
    return parser



if __name__ == "__main__":
    parser = setup_parser()
