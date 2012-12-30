Simplify Writing CLI Apps

Usage:
simpleparse

parser = get_parser()
parser.add_argument(...)

subparser = get_subparser()


parser = setup_parser()


commands.py

def foo(options):
    hello...


arguments.py
-------------
This contains configuration for argument parsers as a list of
dictionaries

from simpleparse import PARSER, SUBPARSERS

PARSER = [
    {
    }
]
SUBPARSERS = [
    {
    }
]


commands.py
------------
This contains the commands executed by parser and subparser. By default,
each command executes a function as the same name as the cmd


