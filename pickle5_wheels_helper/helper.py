import os
import pkg_resources
import sys

def try_install_pickle5():
    should_install_pickle5 = False
    try:
        version_info = pkg_resources.require("pickle5")
        version = tuple(int(n) for n in version_info[0].version.split("."))
        if version < (0, 0, 11):
            should_install_pickle5 = True
    except pkg_resources.DistributionNotFound:
        should_install_pickle5 = True
    if should_install_pickle5:
        print("Count not find pickle5 >= 0.0.11 which is required. Trying to install one from prebuilt wheels...")
        rv = os.system(f'{sys.executable} -m pip install --no-index --find-links=https://github.com/suquark/pickle5-backport/releases/tag/0.0.11 pickle5')
        if rv != 0:
            raise Exception("Failed to install pickle5.")
