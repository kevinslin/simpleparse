import os
import sys

from simpleparse import colors
from simpleparse.settings import *

def check_path(src, force = False):
    """
    Check if path exists. Return true if available.
    If not, offer user a chance to delete
    >>> os.path.exists(__file__)
    True
    >>> os.path.exists("badpath")
    False
    """
    if os.path.exists(src):
        print("%s exists" % src)
        resp = ""
        if force is False:
            resp = raw_input("Overwrite?[y|n] (n default):")
        if (resp.lower() == "y") or force:
            print("overwriting!")
            if (os.path.isdir(src)):
                #TODO: check if dir is empty
                os.rmdir(src)
            else:
                os.remove(src)
        else:
            return False
    return True

def error_msg(msg):
    """
    return with error msg
    """
    print(colors.red(msg))
    return ERROR


def store_true(name, **kwargs):
    """
    Store true option for argparse. Sets default to be false

    @params:
    name - name of arg, multiple names separated by "|" key
    help - help message
    default - default value
    >>> res = store_true("-e|--executable", help="foo")
    >>> sorted(res.keys())
    ['action', 'default', 'help', 'name']
    >>> map(lambda x: res[x], sorted(res.keys()))
    ['store_true', 'False', 'foo', ['-e', '--executable']]
    """
    out = {}
    out['name'] = name.split("|")
    out['action'] = 'store_true'
    out['default'] = kwargs.get('default', "False")
    out['help'] = kwargs.get('help', "")
    return out
