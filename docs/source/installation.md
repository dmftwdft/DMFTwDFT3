# Installation

DMFTwDFT3 is configured for Python 3.11 environments.

The installation has three parts,

1. Create the Python environment.
2. Choose and edit the root `Makefile.in` build configuration.
3. Run `setup.py`, which builds the internal and external components and installs them into `bin`. This step also sets up the environmental variables.

## Python Environment

Recommended environment files are provided in the repository root,

- Linux: `environment.yml`
- macOS: `environment.macos.yml`

For example, on Linux:

```bash
mamba env create -f environment.yml
mamba activate dmft
```

## Build Configuration

Copy one template from `config` to the repository root as `Makefile.in`, then edit paths and compiler choices for your machine.

```bash
cp config/Makefile.in.gnu Makefile.in
python setup.py
```

Available templates,

- `config/Makefile.in.gnu`: GNU compilers on Linux systems.
- `config/Makefile.in.intel`: Intel oneAPI compilers on Linux systems.
- `config/Makefile.in.mac`: macOS Apple Silicon/Homebrew OpenMPI build.

The root `Makefile.in` is the user-managed build configuration that governs the compilation of DMFTwDFT and its dependencies. `setup.py` regenerates internal build files such as `sources/make.inc` and the staged eDMFT `Makefile.in` from the root file. Do not edit generated build files unless you are debugging a build.

The compiled-library dependencies include,

- GSL
- LAPACK
- BLAS
- FFTW
- MPI

### Linux GNU

For a GNU compiler stack, start from,

```bash
cp config/Makefile.in.gnu Makefile.in
```

Check that `Makefile.in` points to the correct BLAS, LAPACK, GSL, FFTW, and MPI locations on your system. The template assumes common Linux-style library paths; adjust `LALIB`, `GSLLIB`, compiler commands, and additional flags as needed.

The GNU template assumes that `liblapack.a`, `libblas.a`, and GSL libraries are installed in `/usr/local/lib`. If your system uses different paths, modify `LALIB` and `GSLLIB` in `Makefile.in`. Use `FFLAGSEXTRA` for additional compiler flags required by your compiler or platform.

### Linux Intel OneAPI

For Intel oneAPI compilers on a cluster, start from,

```bash
cp config/Makefile.in.intel Makefile.in
```

Most of the necessary libraries for the Intel setup will come from the Intel MKL library. Ensure that \$MKLROOT is set correctly in your environment.

### macOS Apple Silicon

For Apple Silicon, start from:

```bash
mamba env create -f environment.macos.yml
mamba activate dmft
cp config/Makefile.in.mac Makefile.in
python setup.py
```

Use one MPI implementation end-to-end. The macOS template is intended for Homebrew OpenMPI, so use Homebrew `mpirun`, Homebrew MPI compiler wrappers, and binaries/extensions linked to Homebrew OpenMPI.

Keep every compiled component on the same architecture and MPI stack. On Apple Silicon, use Homebrew OpenMPI consistently for `mpirun`, `mpi4py`, DMFTwDFT, CTQMC, Wannier90, and DFT interfaces.

Do not mix Homebrew OpenMPI with conda MPICH-linked components. In particular, make sure these components use the same MPI ABI:

- `mpi4py`
- `dmft.x`
- `dmft_dos.x`
- `dmft_ksum_band`
- `dmft_ksum_partial_band`
- `ctqmc`
- Wannier90 executables
- DFT executables launched under MPI

On Apple Silicon, also keep every compiled component native `arm64`. Do not mix `x86_64` Wannier90, SIESTA, or CTQMC binaries with an `arm64` Python environment and libraries.

## Setup Output

If compilation succeeds, the following executables and libraries are copied to `bin`:

- `dmft.x`: performs the DMFT k-point sum and computes `G_loc.out` and `Delta.inp`.
- `dmft_dos.x`: performs DOS calculation.
- `dmft_ksum_band`: performs band-structure calculation.
- `dmft_ksum_partial_band`: performs projected band-structure calculation.
- `fort_kpt_tools.so`: Fortran-based k-point utility module.
- `ctqmc`: CTQMC impurity solver.
- `gaunt.so`, `dpybind.so`, `maxent_routines.so`, and related impurity/maxent helpers.

## Shell Setup

`setup.py` automatically updates your default shell startup file so the main commands and utilities are available from the shell. It adds `bin` and `utilities` to `PATH`, and adds `bin` to `PYTHONPATH` for DMFTwDFT Python imports:

- `~/.zshrc` when `$SHELL` is zsh
- `~/.bashrc` otherwise

The block looks like this:

```bash
# >>> DMFTwDFT setup >>>
export PATH="/path/to/DMFTwDFT3/utilities/:$PATH"
export PATH="/path/to/DMFTwDFT3/bin/:$PATH"
export PYTHONPATH="/path/to/DMFTwDFT3/bin/:$PYTHONPATH"
# <<< DMFTwDFT setup <<<
```

Restart your shell after setup, or source the file printed by `setup.py`.

## Wannier90

DMFTwDFT requires `wannier90.x` and `w90chk2chk.x` to be available in `bin` or otherwise resolvable in your environment. You can get them from [Wannier90](http://www.wannier.org/). VASP workflows also require VASP to be compiled with Wannier90 support.

```{note}
`w90chk2chk.x` has historically been more reliable with Wannier90 v2.1.0 than with some newer Wannier90 releases.
```

For MPI workflows, build Wannier90 against the same MPI implementation used by DMFTwDFT and the DFT code.

## Library Mode for charge self-consistent DFT+DMFT calculations

The compilation also generates `libdmft.a`, which can be linked into DFT codes to enable full charge-self-consistent DFT+DMFT calculations. Otherwise, calculations are self-consistent only within DMFT (one-shot DMFT).

For VASP,

1. Generate `libdmft.a` by compiling DMFTwDFT.
2. Add `libdmft.a` and required libraries/objects to the VASP `makefile.include` link line.
3. Install VASP once before modifying source files.
4. Copy the modified `mlwf.F` from `sources/CSC-mods` into the VASP source tree and rebuild to create dependencies.
5. Copy the other required modified files, such as `charge.F`, `electron.F`, `main.F`, and `us.F`, from `sources/CSC-mods`.
6. Recompile VASP, rename the executable to `vaspDMFT`, and copy it to the DMFTwDFT `bin` directory.

More information on library mode can be found in {ref}`labellibrary`.
