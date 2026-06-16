#!/usr/bin/env python3

import os
import tomllib


INPUT_FILE = "input.toml"

_PC_COMMENTS = {
    "exe": "# Name of impurity solver",
    "beta": "# Inverse temperature",
    "M": "# Number of Monte Carlo steps",
    "nom": "# number of Matsubara frequency points to sample",
    "svd_lmax": "# number of SVD functions to project the solution",
    "tsample": "# how often to record the measurements",
    "aom": "# number of frequency points to determin high frequency tail",
    "warmup": "# Warmup",
    "GlobalFlip": "# Global flip",
    "Ncout": "# Ncout",
    "Naver": "# Naver",
}


def load_input(input_path=INPUT_FILE):
    """Loads input.toml and returns the legacy p, pC, pD objects."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(
            "Missing {0}. Run from a calculation directory containing {0}.".format(
                input_path
            )
        )

    with open(input_path, "rb") as fp:
        data = tomllib.load(fp)

    missing_sections = [section for section in ("p", "pC", "pD") if section not in data]
    if missing_sections:
        raise KeyError(
            "Missing required section(s) in {0}: {1}".format(
                input_path, ", ".join(missing_sections)
            )
        )

    p = data["p"]
    p.setdefault("kmeshtol", 1e-7)
    p.setdefault("sig_tol", 1e-3)
    pC = {key: [value, _PC_COMMENTS.get(key, "")] for key, value in data["pC"].items()}
    pD = data["pD"]
    return p, pC, pD
