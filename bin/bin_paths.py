#!/usr/bin/env python3

"""Filesystem locations for DMFTwDFT executables, scripts, and data files.

Everything DMFTwDFT runs or reads at runtime is installed next to these modules,
so the directory is derived from this file rather than configured by the user.
"""

import os

_BIN_DIR = os.path.dirname(os.path.abspath(__file__))


def bin_path(name):
    """Absolute path to a file installed in the DMFTwDFT bin directory.

    Use for files DMFTwDFT installs itself (scripts, data). Use bin_exec for
    executables that may instead be provided by the system.
    """
    return os.path.join(_BIN_DIR, name)


def bin_exec(name):
    """Resolve an external executable (wannier90, DFT codes) against bin.

    Commands are run under 'cd <dir> &&', so an absolute path is required for
    executables kept in bin. Falls back to the bare name when the executable is
    not in bin, which keeps system or module-provided builds resolvable on PATH.
    """
    path = bin_path(name)
    if os.access(path, os.X_OK) and not os.path.isdir(path):
        return path
    return name
