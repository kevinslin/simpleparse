import unittest
import simpleparse

def foo(options):
    return "foo"

class TestBaseClass(unittest.TestCase):

    def setUp(self):
        self.parser = {
                "description":"parser description",
                "arguments":[
                    {
                        "name":"arg1"
                    },
                    {
                        "name":"--arg2",
                        "nargs":"+"
                        }
                    ]
                }
        self.subparser = {
                "help":"subparser help"
                }
        self.subcommands= [
                {
                    "name":"foo",
                    "description":"the foo command"
                    }
                ]

    def test_parser(self):
        parser = self.parser
        p = simpleparse.get_parser(**parser)
        self.assertEqual(p.description, "parser description",
                "set parser description")
        ret = p.parse_args(["arg1_param"])
        self.assertEqual(ret.arg1, "arg1_param",
                "argument set")
        self.assertEqual(ret.arg2, None, "argument not set")

    def test_subparser(self):
        p = simpleparse.get_parser(**self.parser)
        sp = simpleparse.get_subparser(p, **self.subparser)
        self.assertEqual(sp.help, self.subparser['help'], "help message set")

    def test_subcommands(self):
        sc = simpleparse.get_subcommands(self.subcommands)
        self.assertEqual(sc, {"foo":self.subcommands[0]},
                "proper subcommands set")

    def test_setup_parser(self):
        p = simpleparse.setup_parser(
                parser = {},
                subparser = self.subparser,
                subcommands = self.subcommands,
                funcs = globals())
        ret = p.parse_args(["foo"])
        self.assertEqual(ret.fun(ret), "foo", "func returns right value")

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
