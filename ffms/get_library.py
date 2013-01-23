"""Load shared libraries
"""
#   © 2012 spirit <hiddenspirit@gmail.com>
#
#   This program is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published
#   by the Free Software Foundation, either version 3 of the License,
#   or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty
#   of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#   See the GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>.

import ctypes
import os
from ctypes.util import find_library


__all__ = ["get_library"]


def get_library(name, mode=ctypes.DEFAULT_MODE, handle=None,
                use_errno=False, use_last_error=False, *,
                lib_name=None,
                win_format="lib{}.dll", win64_format=None,
                win_class_name="CDLL", win_attr_format=None):
    """Find and load a shared library.
    """
    library_path = get_library_path(name, win_format, win64_format)
    if not library_path:
        if not lib_name:
            lib_name = name
        raise OSError("can’t find {!r} library".format(lib_name))
    return load_library(library_path, mode, handle, use_errno, use_last_error,
                        win_class_name, win_attr_format)


if os.name == "nt":
    import platform
    import re
    import sys

    def get_bit_architecture():
        if sys.platform == "cli" or sys.platform.startswith("java"):
            return int(re.match("^(\d+)", platform.architecture()[0]).group(1))
        try:
            return int.bit_length(sys.maxsize) + 1
        except (TypeError, AttributeError):
            return 64 if sys.maxsize > (1 << 32) else 32

    if get_bit_architecture() == 64:
        def get_win_format(win_format, win64_format):
            return win64_format or win_format
    else:
        def get_win_format(win_format, win64_format):
            return win_format

    def get_library_path(name, win_format, win64_format):
        win_formats = get_win_format(win_format, win64_format)
        if isinstance(win_formats, str):
            win_formats = [win_formats]
        absdir = lambda p: os.path.dirname(os.path.abspath(p))
        try:
            script_dirs = [absdir(__file__)]
        except NameError:
            script_dirs = []
        script_dirs.append(absdir(sys.argv[0]))
        for win_format in win_formats:
            dll_name = win_format.format(name)
            for script_dir in script_dirs:
                lib_path = os.path.join(script_dir, dll_name)
                if os.path.isfile(lib_path):
                    return lib_path
            lib_path = find_library(dll_name)
            if lib_path:
                return lib_path

    def load_library(library_path, mode, handle, use_errno, use_last_error,
                     win_class_name, win_attr_format):
        library_class = getattr(ctypes, win_class_name)
        cwd = os.getcwd()
        os.chdir(os.path.dirname(library_path) or ".")
        try:
            lib = library_class(library_path, mode, handle,
                                use_errno, use_last_error)
            if win_attr_format:
                class LibWithAttrFormat:
                    """Library with attribute formatter
                    """
                    def __init__(self, lib, attr_format):
                        self.__lib = lib
                        self.__attr_format = attr_format

                    def __repr__(self):
                        return "{}({!r}, {!r})".format(
                            self.__class__.__name__,
                            self.__lib, self.__attr_format)

                    def __getattr__(self, name):
                        try:
                            return getattr(self.__lib,
                                           self.__attr_format.format(name))
                        except AttributeError:
                            return getattr(self.__lib, name)

                lib = LibWithAttrFormat(lib, win_attr_format)
            return lib
        finally:
            os.chdir(cwd)

else:
    def get_library_path(name, win_format, win64_format):
        return find_library(name)

    def load_library(library_path, mode, handle, use_errno, use_last_error,
                     win_class_name, win_attr_format):
        return ctypes.CDLL(library_path, mode, handle,
                           use_errno, use_last_error)
