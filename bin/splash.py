#!/usr/bin/env python3

import sys

version = "2.3"
date = "Jul 11, 2026"


def welcome():
    art = """
 ____  __  __ _____ _____          ____  _____ _____
|  _ \|  \/  |  ___|_   _|_      _|  _ \|  ___|_   _|
| | | | |\/| | |_    | | \ \ /\ / / | | | |_    | |
| |_| | |  | |  _|   | |  \ V  V /| |_| |  _|   | |
|____/|_|  |_|_|     |_|   \_/\_/ |____/|_|     |_|

    """
    pversion = ".".join(map(str, sys.version_info[:3]))
    print(art)
    print(("Python 3 version running on Python %s." % pversion))
    print(
        "\n--- An open-source framework to treat strongly correlated materials using DMFT ---"
    )
    print(("\nVersion %s updated on %s.\n" % (version, date)))
    print(
        "Please cite:\n \
Vijay Singh, Uthpala Herath, Benny Wah, Xingyu Liao, Aldo H. Romero, Hyowon Park.,\n \
DMFTwDFT: An open-source code combining Dynamical Mean Field Theory with various Density Functional Theory packages.,\n \
Computer Physics Communications 261, 107778 (2021). https://doi.org/10.1016/j.cpc.2020.107778\n"
    )

    separator_art = """
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
        """
    print(separator_art)

    return
