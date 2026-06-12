# Installation

DMFTwDFT3 is configured for Python 3.11 environments. Use an already relaxed structure as input when running workflows that do not support ionic relaxation.

Install the Python and compiled-library dependencies before installing DMFTwDFT. The recommended environment files are:

- Linux: `environment.yml`
- macOS: `environment.macos.yml`

For example, on Linux:

```bash
mamba env create -f environment.yml
mamba activate dmft
```

The core Python dependencies include:

- `matplotlib`
- `numpy`
- `scipy`
- `mpi4py`
- `numba`
- `pybind11`

The core compiled-library dependencies include:

- GSL
- LAPACK
- BLAS
- FFTW

The directory structure is:

```text
DMFTwDFT3
├── bin
├── config
├── docs
├── examples
├── manuals
├── scripts
├── sphinx
├── support_packages
└── sources
    ├── src
    ├── dmft_ksum
    ├── fort_kpt_tools
    └── CSC-mods
```

The following sections describe the procedure to compile the different components required to run DMFTwDFT. Once the executables and libraries have been compiled, they should be inside the `bin` directory.

## Compiling Sources

First copy a desired `Makefile.in` version from the `config` directory to the repository root based on the compiler you wish to use. You may have to specify the locations of the GSL, LAPACK, and other libraries.

After copying one of `config/Makefile.in.intel`, `config/Makefile.in.gnu`, or `config/Makefile.in.mac` to `Makefile.in` and editing it for your machine, run:

```bash
python setup.py
```

This should compile the following executables and libraries and copy them to the `bin` directory:

- `dmft.x`: achieves DMFT self-consistency. It performs the $k$-point sum and computes the local Green's function (`G_loc.out`) and hybridization function (`Delta.inp`).
- `dmft_dos.x`: performs DOS calculation.
- `dmft_ksum_band`: performs band structure calculation.
- `dmft_ksum_partial_band`: performs projected band structure calculation.
- `fort_kpt_tools.so`: Fortran-based k-points calculation module.

If you want to install them manually, keep `Makefile.in` at the repository root as your editable source of truth and let `setup.py` regenerate `sources/make.inc` from it before building inside `sources`.

## External Libraries and Executables

DMFTwDFT uses the CTQMC impurity solver and Max-entropy routines developed by Professor Kristjan Haule at Rutgers University, available with the [EDMFTF](http://hauleweb.rutgers.edu/tutorials/index.html) package. The following libraries and programs are used:

- `ctqmc`
- `gaunt.so`
- `gutils.so`
- `skrams`
- `maxent_routines.so`

If the automated compilation with `setup.py` is successful, these are found in the `bin` directory.

## Wannier90 Library

DMFTwDFT requires `wannier90.x` and `w90chk2chk.x` to be in the `bin` directory. You can get them from [Wannier90](http://www.wannier.org/). VASP should be recompiled with the Wannier90 library.

```{note}
`w90chk2chk.x` seems to be problematic with Wannier90 v3.0+. It has been tested successfully with v2.1.0.
```

## Path Variables

Finally, the location of the DMFTwDFT `bin` directory should be added to the `$PATH` and `$PYTHONPATH` environment variables in your shell configuration.

## Compiling Library Mode for Full Charge-Self-Consistent DFT+DMFT Calculations

The above compilation also generates `libdmft.a`, which can be used to link DMFTwDFT to DFT codes to enable full charge self-consistent DFT+DMFT calculations. Otherwise, the calculations can only be run for self-consistency within DMFT. For VASP, follow these steps to compile for self-consistency.

1. Generate `libdmft.a` by compiling the source code.
2. Change the VASP `makefile.include` file. Specify libraries and/or objects to be linked against in the usual ways:

```makefile
LLIBS += -Lparser -lparser -lstdc++ /home/uthpala/wannier90/wannier90-1.2/libwannier.a \
         /home/uthpala/Dropbox/git/DMFTwDFT/sources/libdmft.a
```

3. Before modifying the VASP source code, install VASP as-is by following the VASP installation instructions.
4. Copy the modified `mlwf.F` VASP file from the `sources/CSC-mods` directory to the VASP source directory and install VASP again. This step creates dependencies for the next step.
5. Copy the other modified or required VASP files, such as `charge.F`, `electron.F`, `main.F`, and `us.F`, from the `sources/CSC-mods` directory to the VASP source directory.
6. Recompile VASP. Then rename this VASP executable to `vaspDMFT` and copy it to the DMFTwDFT `bin` directory.

More information on the library mode can be found in {ref}`labellibrary`.
