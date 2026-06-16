# Examples

The `/examples` directory contains starting points for several DMFTwDFT workflows. Copy an example directory to a separate run directory before editing inputs or launching a calculation.

Before running any example:

- Build and install DMFTwDFT as described in {doc}`../installation`.
- Set `path_bin` in `input.toml` to your local DMFTwDFT `bin` directory.
- Edit `para_com.dat` and optional `para_com_dft.dat` for your MPI launcher.
- Provide licensed or site-specific files that are not committed, such as VASP `POTCAR` files or Quantum Espresso pseudopotentials.
- Use the same MPI stack for Python, DMFTwDFT executables, impurity solvers, Wannier90, and DFT executables.

```{note}
The PDF manuals in `/examples` are useful historical references, but some commands and file names in them predate the current `input.toml`, `DMFT.py`, and `postDMFT.py` workflow. The example pages use the current names where they differ from the PDFs.
```

```{toctree}
:maxdepth: 1
:caption: Bundled Examples

srvo3_vasp
srvo3_siesta
srvo3_qe
srvo3_qe_aiida
lanio3_vasp
library_mode
```
