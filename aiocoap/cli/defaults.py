# This file is part of the Python aiocoap library project.
#
# Copyright (c) 2012-2014 Maciej Wasilak <http://sixpinetrees.blogspot.com/>,
#               2013-2014 Christian Amsüss <c.amsuess@energyharvesting.at>
#
# aiocoap is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

"""This helper script can be used to easily inspect aiocoap's environment
autodetection (ie. whether all modules required for particular subsystems are
available, losely corresponding to the "features" made available through
setup.py); run it as `python3 -m aiocoap.cli.defaults`."""

import sys
from aiocoap.meta import version
from aiocoap.defaults import *
import argparse

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--expect-all", help="Exit with an error unless all subsystems are available", action='store_true')
    p.add_argument('--version', action='version', version=version)
    args = p.parse_args()

    error = 0

    print("Python version: %s" % sys.version)
    print("aiocoap version: %s" % version)
    print("Modules missing for subsystems:")
    missmods = [dtls_missing_modules, oscore_missing_modules, linkheader_missing_modules, prettyprint_missing_modules]
    for m in missmods:
        name = m.__name__[:-len("_missing_modules")]
        missing = m()
        if missing and args.expect_all:
            error = 1
        print("    %s: %s" % (name, "everything there" if not missing else "missing " + ", ".join(missing)))
    print("Python platform: %s" % sys.platform)
    print("Default server transports:  %s" % ":".join(get_default_servertransports(use_env=False)))
    print("Selected server transports: %s" % ":".join(get_default_servertransports()))
    print("Default client transports:  %s" % ":".join(get_default_clienttransports(use_env=False)))
    print("Selected client transports: %s" % ":".join(get_default_clienttransports()))

    sys.exit(error)