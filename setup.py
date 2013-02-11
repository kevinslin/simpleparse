from distutils.core import setup

PACKAGE = "simpleparse"
NAME = "simpleparse"
DESCRIPTION = "Simplifying making CLI apps"
AUTHOR = "Kevin S  Lin"
AUTHOR_EMAIL = "kevinslin8@gmail.com"
URL = ""
VERSION = __import__(PACKAGE).__version__


setup(name = 'simpleparse',
      version = VERSION,
      description = DESCRIPTION,
      author = 'Kevin S Lin',
      author_email = 'kevinslin8@gmail.com',
      url = 'kevinslin.com',
      long_description = DESCRIPTION,
      packages = ['simpleparse']
      )
