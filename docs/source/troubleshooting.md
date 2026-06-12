# Troubleshooting

This page collects common installation and runtime failures and the checks that usually identify the cause.

## MPI Stack Mismatch

MPI components must use the same MPI implementation. A common macOS failure is launching with Homebrew OpenMPI while `mpi4py` or a compiled executable is linked against conda MPICH.

Typical symptoms include:

```text
Runtime environment uses unsupported PMI version PMIx
```

or MPI jobs that fail immediately before entering DMFTwDFT, CTQMC, Wannier90, or the DFT executable.

Checks:

```bash
which mpirun
mpirun --version
python -c "from mpi4py import MPI; print(MPI.Get_library_version())"
```

On macOS with Homebrew OpenMPI, linked libraries should resolve to Homebrew OpenMPI, for example `libmpi.40.dylib`, not conda MPICH libraries such as `libmpi.12.dylib`.

## Apple Silicon Architecture Mismatch

On Apple Silicon, keep every compiled component native `arm64` unless you intentionally run a complete `x86_64` stack under Rosetta.

Checks:

```bash
file bin/dmft.x
file bin/ctqmc
file /path/to/wannier90.x
```

Do not mix `x86_64` Wannier90, SIESTA, CTQMC, or MPI libraries with an `arm64` Python environment.

## Harmless Stderr From Successful Programs

Some compilers and runtimes print warnings or floating-point status notes to `stderr` even when the command succeeds. One example is:

```text
Note: The following floating-point exceptions are signalling: IEEE_OVERFLOW_FLAG
```

DMFTwDFT checks command return codes and expected output files instead of treating any `stderr` text as fatal. If you see this message but the expected output file is created, it is usually diagnostic rather than a failed calculation.

Examples of expected files:

- Wannier90 preprocessing: `<seed>.nnkp`
- SIESTA: `<seed>.out`
- DMFT DOS: `dos/G_loc.out`
- Band calculations: `bands/Gk.out`
- Analytic continuation: `ac/Sig.out`

## Fresh SIESTA Runs Stop After Wannier90 Preprocessing

For SIESTA workflows, DMFTwDFT first generates `wannier90.win`, runs `wannier90 -pp`, then launches SIESTA. A successful preprocessing step writes `<seed>.nnkp`.

If the workflow stops after `wannier90.win generated`, check:

```bash
ls -l <seed>.nnkp
wannier90.x -pp <seed>
```

If `<seed>.nnkp` exists and the command returns success, SIESTA should be able to proceed. The warning-only `stderr` case is handled by current DMFTwDFT, but older checkouts may exit early.

## Missing Or Stale Shell Setup

After setup, `DMFT.py` and `postDMFT.py` should be runnable from calculation directories.

Check:

```bash
which DMFT.py
python -c "import Fileio; print(Fileio.__file__)"
```

If these fail, restart the shell or source the startup file printed by `setup.py`.

For zsh this is usually:

```bash
source ~/.zshrc
```

For bash this is usually:

```bash
source ~/.bashrc
```

## Generated Build Files

The root `Makefile.in` is the editable build configuration. `setup.py` regenerates internal build files from it, including `sources/make.inc` and staged eDMFT makefiles.

If a build fails, update the root `Makefile.in` and rerun:

```bash
python setup.py
```

Only edit generated files directly when debugging a build and expecting those edits to be overwritten by the next setup run.

## Checking Linked MPI Libraries

On macOS, use `otool` to inspect dynamic libraries:

```bash
otool -L bin/dmft.x
otool -L bin/ctqmc
python - <<'PY'
import mpi4py, pathlib
print(pathlib.Path(mpi4py.__file__).parent)
PY
```

For the `mpi4py` extension, inspect the `.so` file inside the printed directory. Homebrew OpenMPI builds should link to `/opt/homebrew/opt/open-mpi/lib/libmpi.40.dylib` or equivalent Homebrew OpenMPI paths.
