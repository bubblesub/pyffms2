import os
import re
import sys

import setup


if os.name == "nt":
    import platform
    import shutil

    def get_bit_architecture():
        if sys.platform == "cli" or sys.platform.startswith("java"):
            return int(re.match("^(\d+)", platform.architecture()[0]).group(1))
        try:
            return int.bit_length(sys.maxsize) + 1
        except (TypeError, AttributeError):
            return 64 if sys.maxsize > 2 ** 32 else 32

    DLL_PATH = (r"windows\x64\ffms2.dll" if get_bit_architecture() == 64
                else r"windows\ffms2.dll")

    def hook(config):
        shutil.copy(DLL_PATH, "ffms\\")
        config["files"].setdefault("package_data", "")
        config["files"]["package_data"] += "\nffms = ffms2*.dll"

else:
    import subprocess
    from ctypes.util import find_library

    def hook(config):
        externals = setup.get_cfg_value(
            config, "metadata", "requires-external")

        for external in externals:
            match = re.match("^lib(\w+)(-\d.*)?$", external)
            if not match:
                continue
            name = match.group(1)
            path_name = find_library(name)
            if path_name:
                continue
            if subprocess.call(["which", "apt-get"]):
                raise OSError("can't find {!r} library".format(name))
            print("Installing {!r}...".format(external))
            subprocess.call(["sudo", "apt-get", "install", external])
