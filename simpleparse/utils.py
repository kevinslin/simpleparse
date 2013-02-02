import os
import shutil
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
                try:
                    os.rmdir(src)
                except OSError:
                    resp = raw_input(
                            "Dir not empty. Overwrite anyways?[y|n]:")
                    if (resp.lower() == 'y') or force:
                        shutil.rmtree(src)
                    else:
                        return False
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


def store_false(name, **kwargs):
    """
    >>> res = store_false("-e|--executable", help="foo")
    >>> sorted(res.keys())
    ['action', 'default', 'help', 'name']
    >>> map(lambda x: res[x], sorted(res.keys()))
    ['store_false', 'True', 'foo', ['-e', '--executable']]
    """
    return store_action(name, action = "store_false", default = "True", **kwargs)

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
    >>> res2 = store_true("-e", help="foo")
    >>> sorted(res2.keys())
    ['action', 'default', 'help', 'name']
    >>> map(lambda x: res2[x], sorted(res2.keys()))
    ['store_true', 'False', 'foo', ['-e']]
    """
    return store_action(name, action = "store_true", default = "False", **kwargs)

def append(name, **kwargs):
    """
    >>> res = append("-e|--executable")
    >>> sorted(res.keys())
    ['action', 'name']
    >>> [res[k] for k in sorted(res.keys())]
    ['append', ['-e', '--executable']]
    """
    return store_action(name, action = "append", **kwargs)

def store_const(name, action = None, **kwargs):
    """
    >>> res = store_const("-e|--executable", const='foo')
    >>> sorted(res.keys())
    ['action', 'const', 'name']
    >>> [res[k] for k in sorted(res.keys())]
    ['store_const', 'foo', ['-e', '--executable']]
    """
    # Exception if const value isn't set
    if kwargs.get('const') is None:
        kwargs['const'] = ""
    return store_action(name, action="store_const", **kwargs)

def store_action(name, action = None, **kwargs):
    out = {}
    out['name'] = name.split("|")
    if action is None:
        raise Exception("must specify action")
    out['action'] = action
    set_if_value_not_none(out, 'default', kwargs.get('default'))
    set_if_value_not_none(out, 'const', kwargs.get('const'))
    set_if_value_not_none(out, 'help', kwargs.get('help'))
    return out

### Bash related:
def read_rc(fpath):
    """
    Read key value files from rc file
    """
    out = {}
    with open(fpath) as fh:
        for line in fh:
            u = line.strip("\n").split("=")
            u = [v.strip() for v in u]
            if (len(u) > 1):
                out[u[0]] = u[1]
    return out


### MOVE:

def save_eval(statement, accept = None):
    """
    Eval that only takes certain statements
    >>> save_eval("True")
    True
    >>> save_eval("")
    """
    safe = ["True", "False", ""]
    if (statement == ""):
        return None
    else:
        if (statement in safe):
            return eval(statement)
        else:
            raise Exception("statement %s not in safe eval"
                    % statement)

def set_if_value_not_none(_dict, key, value):
    """
    Only set if value is not none
    """
    if (value is not None):
        _dict[key] = value
