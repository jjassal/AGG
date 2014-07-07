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
        "includes":["sip",],
        "excludes":['_ssl','pyreadline','difflib', 'doctest', 'optparse', 'pickle'],
        
    }
}

setup(
    name="Ayakashi",
    windows=[{

    "script":"AyakashiProxy.py",
    # "icon_resources": [(0, "icon.png")]
    }],
    options=option,
    # zipfile=None
    )

