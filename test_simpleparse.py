import unittest
import simpleparse


def foo(options):
    return "foo"


class TestBaseClass(unittest.TestCase):

    def setUp(self):
        simpleparse.SUBPARSERS = [
                {
                    "name":"foo",
                    "description":"the foo command"
                    }
                ]

    def test_foo_subcommand(self):
        p = simpleparse.setup_parser(
            subparsers=simpleparse.SUBPARSERS,
            commands = globals())
        ret = p.parse_args(["foo"])
        self.assertEqual(ret.fun(ret), "foo")

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
