"""Load shared libraries.
"""
import ctypes
import os
from ctypes.util import find_library


__all__ = ["get_library"]


def get_library(name, mode=ctypes.DEFAULT_MODE, handle=None,
                use_errno=False, use_last_error=False, *,
                win32_format="lib{}.dll", win64_format="lib{}.dll",
                win_class_name="CDLL"):
    """Find and load a shared library.
    """
    library_path = get_library_path(name, win32_format, win64_format)
    if not library_path:
        raise OSError("can’t find {!r} library".format(name))
    return load_library(library_path, mode, handle, use_errno, use_last_error,
                        win_class_name)


if os.name == "nt":
    import sys

    if sys.maxsize == 2 ** 31 - 1:
        def get_win_format(win32_format, win64_format):
            return win32_format
    else:
        def get_win_format(win32_format, win64_format):
            return win64_format

    def get_library_path(name, win32_format, win64_format):
        win_formats = get_win_format(win32_format, win64_format)
        if isinstance(win_formats, str):
            win_formats = [win_formats]
        for win_format in win_formats:
            dll_name = win_format.format(name)
            if os.path.isfile(dll_name):
                lib_path = dll_name
            else:
                lib_path = find_library(dll_name)
                if not lib_path:
                    try:
                        script_path = os.path.abspath(__file__)
                    except NameError:
                        pass
                    else:
                        path = os.path.join(os.path.dirname(script_path),
                                            dll_name)
                        if os.path.isfile(path):
                            lib_path = path
            if lib_path:
                break
        return lib_path

    def load_library(library_path, mode, handle, use_errno, use_last_error,
                     win_class_name):
        library_class = getattr(ctypes, win_class_name)
        cwd = os.getcwd()
        os.chdir(os.path.dirname(library_path) or ".")
        try:
            return library_class(library_path, mode, handle,
                                 use_errno, use_last_error)
        finally:
            os.chdir(cwd)

else:
    def get_library_path(name, win32_format, win64_format):
        return find_library(name)

    def load_library(library_path, mode, handle, use_errno, use_last_error,
                     win_class_name):
        return ctypes.CDLL(library_path, mode, handle,
                           use_errno, use_last_error)
