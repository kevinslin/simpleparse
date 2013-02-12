Simplify Writing CLI Apps
=========================

**DISCLAIMER: This is not yet ready for production, not in the slightest bit**

Usage
-----

.. code-block:: pycon

    from simpleparse import setup_parser
    import commands

    p = setup_parser(
        parser = <parser>,
        subcommands = <subcommands>,
        funcs = vars(commands)
        )
    args = p.parse_args(sys.argv[1:])
    if (args.fun):
        args.fun(args)
    else:
        # custom implementation
    # commands.py

    def foo(options):
        hello...


New Usage
---------

.. code-block:: pycon

    from simpleparse import setup_parser
    p = setup_parser(__file__)
    p.parse()
    res = p.execute()

By default, will look for parser and subparser in arguments.py
Will import commands from "commands" inside module directory.


arguments.py
------------
This contains configuration for argument parsers as a list of
dictionaries

.. code-block:: pycon

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
-----------
This contains the commands executed by parser and subparser. By default,
each command executes a function as the same name as the cmd
