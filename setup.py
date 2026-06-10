#!/usr/bin/env python3
"""DMFTwDFT setup.

Copy one of the bundled templates from `config/` to `./Makefile.in`, edit it
as needed for your machine, and then run `setup.py`.

All the executables will be copied to the bin directory.
Don't forget to install wannier90 and recompile VASP with wannier90.
Also copy wannier90.x and w90chk2chk.x to the bin directory.

"""

import sys
import os
import shutil
import subprocess
import glob
import argparse
import shlex
from argparse import RawTextHelpFormatter
from sysconfig import get_paths

sys.path.insert(1, "./bin")
import splash


DEFAULT_EDMFT_SOURCE = "https://github.com/ru-ccmt/eDMFT.git"


def replace_text(file_path, old, new):
    """Replace text in a file if present."""
    fp = open(file_path, "r")
    data = fp.read()
    fp.close()

    if old in data:
        fo = open(file_path, "w")
        fo.write(data.replace(old, new))
        fo.close()


def read_makefile_vars(makefile_path):
    """Parses simple KEY = VALUE assignments from a makefile."""
    values = {}
    with open(makefile_path, "r") as fp:
        for line in fp:
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.split("#", 1)[0].rstrip()
    return values


def command_executable(command, default):
    """Returns the executable portion of a makefile command assignment."""
    if not command:
        return default
    try:
        parts = shlex.split(command)
    except ValueError:
        parts = command.split()
    return parts[0] if parts else default


def write_internal_make_inc(base_makefile_path, output_path):
    """Generates sources/make.inc from the user-managed root Makefile.in."""
    values = read_makefile_vars(base_makefile_path)

    f90 = values.get("F90", "gfortran").strip()
    mpif90 = values.get("PF90", values.get("MPIF90", f90)).strip()
    cmp_value = values.get("CMP", (sys.executable + " -m numpy.f2py")).strip()
    fcopts = values.get("FFLAGS", values.get("OFLAGS", "-O2")).strip()
    ldopts = values.get("OFLAGS", "-O2").strip()
    libs = values.get("LALIB", values.get("LLIBS", "")).strip()
    comms = "mpi" if values.get("PF90", "").strip() else "serial"

    lines = [
        "# Auto-generated from ../Makefile.in by setup.py.",
        "F90 = %s" % f90,
        "COMMS=%s" % comms,
        "MPIF90=%s" % mpif90,
        "CMP = %s" % cmp_value,
        "",
        "FCOPTS=%s" % fcopts,
        "LDOPTS=%s" % ldopts,
        "",
        "LIBS = %s" % libs,
        "",
    ]

    with open(output_path, "w") as fp:
        fp.write("\n".join(lines))


def stage_external_sources(edmft_source, destination, edmft_ref=None):
    """Clones or copies the requested eDMFT source tree into the local build area."""
    if os.path.exists(destination):
        shutil.rmtree(destination)

    if os.path.isdir(edmft_source):
        src_dir = os.path.join(edmft_source, "src")
        if not os.path.isdir(src_dir):
            raise FileNotFoundError("eDMFT src directory not found: %s" % src_dir)
        shutil.copytree(edmft_source, destination)
        return "local copy"

    clone_cmd = ["git", "clone", "--depth", "1"]
    if edmft_ref:
        clone_cmd.extend(["--branch", edmft_ref])
    clone_cmd.extend([edmft_source, destination])
    subprocess.check_call(clone_cmd)

    src_dir = os.path.join(destination, "src")
    if not os.path.isdir(src_dir):
        raise FileNotFoundError("Cloned eDMFT tree is missing src/: %s" % destination)
    return "git clone"


def write_edmft_makefile(base_makefile_path, edmft_src_dir):
    """Creates the Makefile.in expected by the newer eDMFT tree."""
    with open(base_makefile_path, "r") as fp:
        makefile = fp.read().rstrip() + "\n"

    values = read_makefile_vars(base_makefile_path)
    python_cc = command_executable(values.get("CC"), "gcc")
    python_cxx = command_executable(values.get("C++"), "g++")

    include_dir = os.path.join(edmft_src_dir, "includes")
    python_include = get_paths()["include"]
    safe_f2py_fflags = "--f90flags='-fopenmp -O2'"

    makefile += "DESTDIR = bin\n"
    makefile += "CMP = env SETUPTOOLS_USE_DISTUTILS=stdlib CC={0} CXX={1} FC=gfortran F77=gfortran F90=gfortran NPY_DISTUTILS_APPEND_FLAGS=1 {2} -m numpy.f2py --opt='-O2' --fcompiler=gnu95\n".format(
        python_cc, python_cxx, sys.executable
    )
    makefile += "F2PL = {0}\n".format(safe_f2py_fflags)
    makefile += "PYBND = -I{0} -I{1} -shared -std=c++11 -fPIC\n".format(
        include_dir, python_include
    )

    with open(os.path.join(edmft_src_dir, "Makefile.in"), "w") as fp:
        fp.write(makefile)


def main(args):
    """Installation main function."""

    # call cleanup
    cleanup()

    # print welcome message
    splash.welcome()

    # --------------- COMPILING INTERNAL SOURCES -----------------------------
    base_makefile = "./Makefile.in"
    if not os.path.exists(base_makefile):
        print("Missing ./Makefile.in.")
        print(
            "Copy one of config/Makefile.in.{intel,gnu,mac} to ./Makefile.in and edit it before running setup.py."
        )
        sys.exit(1)

    print("Using local Makefile.in\n")
    write_internal_make_inc(base_makefile, "./sources/make.inc")

    print("Compiling internal sources...\n")
    cmd = "cd sources; make clean; make all > internal.log 2>&1 "
    out, err = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).communicate()

    # Checking if all internal sources have been compiled
    file_list = [
        "dmft.x",
        "dmft_dos.x",
        "libdmft.a",
        "./dmft_ksum/dmft_ksum_band",
        "./dmft_ksum/dmft_ksum_partial_band",
    ]

    result_array = []

    for fi in file_list:
        result = os.path.exists("./sources/" + fi)
        result_array.append(result)
        print("Compiled file %s exists : %s " % (fi, result))

    if all(result_array):
        print("Internal compilation complete.")
    else:
        print(
            "Internal compilation failed! Check internal.log for details. Make sure Makefile.in points to the correct lapack, blas and gsl libraries. You can also build manually inside the sources directory after regenerating sources/make.inc from your local Makefile.in. Run with -ignore to bypass."
        )
        if not args.ignore:
            sys.exit()

    # --------------- COMPILING EXTERNAL SOURCES -----------------------------

    print("\nCompiling external sources...")
    edmft_source = os.path.expanduser(os.path.expandvars(args.edmft_source))
    external_dir = "./sources/eDMFT"
    fetch_mode = stage_external_sources(edmft_source, external_dir, args.edmft_ref)
    print("Prepared eDMFT sources via %s from %s..." % (fetch_mode, edmft_source))

    src_dir = os.path.join(external_dir, "src")
    write_edmft_makefile(base_makefile, src_dir)

    # Compiling ctqmc
    ctqmc_dir = os.path.join(src_dir, "impurity", "ctqmc")
    print("Compiling ctqmc...")
    cmd = "cd " + ctqmc_dir + "; make clean; make ctqmc > ctqmc.log 2>&1"
    out, err = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).communicate()
    if os.path.exists(os.path.join(ctqmc_dir, "ctqmc")):
        print("Complete.\n")
        # Copy to bin directory
        shutil.copy(os.path.join(ctqmc_dir, "ctqmc"), "./bin/")
    else:
        print(
            "ctqmc compilation failed! Check ctqmc.log for details. Run with -ignore to bypass."
        )
        if not args.ignore:
            sys.exit()

    # Compiling atomd (gaunt.so, dpybind.so)
    atomd_dir = os.path.join(src_dir, "impurity", "atomd")
    replace_text(
        os.path.join(atomd_dir, "Makefile"),
        "mv gaunt.*so gaunt.so",
        "test -f gaunt.so || mv gaunt.*so gaunt.so",
    )
    replace_text(
        os.path.join(atomd_dir, "Makefile"),
        "$(CMP) $(F2PL) -c $? -m gaunt ",
        "env FFLAGS='-fopenmp -O2' F90FLAGS='-fopenmp -O2' F77FLAGS='-fopenmp -O2' $(CMP) $(F2PL) -c $? -m gaunt ",
    )
    print("Compiling atomd : gaunt.so, dpybind.so...")
    cmd = "cd " + atomd_dir + "; make clean; make all > atomd.log 2>&1"
    out, err = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).communicate()
    if os.path.exists(os.path.join(atomd_dir, "gaunt.so")) and os.path.exists(
        os.path.join(atomd_dir, "dpybind.so")
    ):
        print("Complete.\n")
        # Copy to bin directory
        shutil.copy(os.path.join(atomd_dir, "gaunt.so"), "./bin/")
        shutil.copy(os.path.join(atomd_dir, "dpybind.so"), "./bin/")
        # Keep the DMFTwDFT-local atom_d.py, which preserves UC.dat output.
        shutil.copy(os.path.join(atomd_dir, "cubic_harmonics.py"), "./bin/")

    else:
        print(
            "atomd compilation failed! Check atomd.log for details. Run with -ignore to bypass."
        )
        if not args.ignore:
            sys.exit()

    # Compiling maxent_routines
    maxent_dir = os.path.join(src_dir, "impurity", "maxent_source")
    replace_text(
        os.path.join(maxent_dir, "Makefile"),
        "$(CMP) -c maxent_routines.f90 -m maxent_routines $(CMPLIBS)",
        "env FFLAGS='-fopenmp -Ofast' F90FLAGS='-fopenmp -Ofast' F77FLAGS='-fopenmp -Ofast' $(CMP) -c maxent_routines.f90 -m maxent_routines $(CMPLIBS)",
    )
    replace_text(
        os.path.join(maxent_dir, "Makefile"),
        "mv maxent_routines.*so maxent_routines.so",
        "test -f maxent_routines.so || mv maxent_routines.*so maxent_routines.so",
    )
    print("Compiling maxent_routines...")
    cmd = "cd " + maxent_dir + "; make clean; make all > maxent_routines.log 2>&1"
    out, err = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).communicate()
    if os.path.exists(os.path.join(maxent_dir, "maxent_routines.so")):
        print("Complete.\n")
        # Copy to bin directory
        shutil.copy(os.path.join(maxent_dir, "maxent_routines.so"), "./bin/")
        # Keep the maxent Python frontends aligned with the staged eDMFT tree.
        shutil.copy(os.path.join(maxent_dir, "maxentropy.py"), "./bin/")
        shutil.copy(os.path.join(maxent_dir, "maxent_run.py"), "./bin/")
    else:
        print(
            "maxent_routines compilation failed! Check maxent_routines.log for details. Run with -ignore to bypass."
        )
        if not args.ignore:
            sys.exit()

    # Compiling skrams
    skrams_dir = os.path.join(src_dir, "impurity", "skrams")
    print("Compiling skrams...")
    cmd = "cd " + skrams_dir + "; make clean; make all > skrams.log 2>&1"
    out, err = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).communicate()
    if os.path.exists(os.path.join(skrams_dir, "skrams")):
        print("Complete.\n")
        # Copy to bin directory
        shutil.copy(os.path.join(skrams_dir, "skrams"), "./bin/")
    else:
        print(
            "skrams compilation failed! Check skrams.log for details. Run with -ignore to bypass."
        )
        if not args.ignore:
            sys.exit()

    # Compilation complete
    print("DMFTwDFT compilation complete!")
    print(
        "Please add the bin directory to $PATH and $PYTHONPATH variables in your .bashrc."
    )
    print("Thank you!")


def cleanup():
    """Cleanup."""
    if os.path.exists("./sources/internal.log"):
        os.remove("./sources/internal.log")
    if os.path.exists("./sources/make.inc"):
        os.remove("./sources/make.inc")
    try:
        for foldername in glob.glob("./sources/eDMFT*"):
            shutil.rmtree(foldername)
    except (FileNotFoundError, IOError):
        pass

    # Cleaning bin folder
    bin_files = [
        "dmft.x",
        "dmft_dos.x",
        "dmft_ksum_band",
        "dmft_ksum_partial_band",
        "fort_kpt_tools.so",
        "ctqmc",
        "gaunt.so",
        "gutils.so",
        "dpybind.so",
        "cubic_harmonics.py",
        "skrams",
        "maxent_routines.so",
        "maxentropy.py",
        "maxent_run.py",
    ]

    for bin_i in bin_files:
        if os.path.exists("./bin/" + bin_i):
            os.remove("./bin/" + bin_i)


if "__main__" == __name__:
    parser = argparse.ArgumentParser(
        description=(
            "DMFTwDFT setup.\nCopy one of config/Makefile.in.{intel,gnu,mac} "
            "to ./Makefile.in, edit it for your machine, and run setup.py."
        ),
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "-ignore",
        help="Ignore compilation errors and continue.",
        action="store_true",
    )
    parser.add_argument(
        "--edmft-source",
        "--edmft-root",
        default=DEFAULT_EDMFT_SOURCE,
        dest="edmft_source",
        help="Local path or git URL for the Python 3 eDMFT source tree.",
    )
    parser.add_argument(
        "--edmft-ref",
        default=None,
        help="Optional git branch or tag to clone for eDMFT.",
    )
    main(parser.parse_args())
