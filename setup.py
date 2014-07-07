__author__ = 'jackyzy823'

from distutils.core import setup
import py2exe
import sys

sys.argv.append("py2exe")

option={
    "py2exe":{
        "compressed":1,
        "optimize":2,
        "bundle_files":1,
        "includes":["sip",]
    }
}

setup(windows=["proxy_gui.py"],options=option,zipfile=None)

