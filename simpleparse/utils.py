def check_path(src, force = False):
    """
    Check if path exists. Return true if available.
    If not, offer user a chance to delete
    """
    if os.path.exists(src):
        print("%s exists" % src)
        resp = ""
        if force is False:
            resp = raw_input("Overwrite?[y|n] (n default):")
        if (resp.lower() == "y") or force:
            print("overwriting!")
            if (os.path.isfile(src)):
                os.remove(src)
            else:
                #TODO: check if dir is empty
                os.path.rmdir(src)
        else:
            return False
    return True


def store_true(name, **kwargs):
    """
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
