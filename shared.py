"""Shared functions
"""

import os.path

def getPysqgBaseDir():
    """Get the base directory of the pysqg package
    """
    import pysqg.shared
    return os.path.split(os.path.abspath(pysqg.shared.__file__))[0]

def getPysqgIncludeDir():
    """Get the base directory of the pyseg include hierarchy
    """
    return os.path.join(getPysqgBaseDir(), "include")