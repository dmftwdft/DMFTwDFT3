# Examples

The [/examples](https://github.com/dmftwdft/DMFTwDFT3/tree/master/examples) directory contains starting points for several DMFTwDFT workflows. Copy an example directory to a separate run directory before editing inputs or launching a calculation.

Before running any example,

- Build and install DMFTwDFT as described in {doc}`../installation`.
- Set `path_bin` in `input.toml` to your local DMFTwDFT `bin` directory.
- Edit `para_com.dat` and optional `para_com_dft.dat` for your MPI launcher.
- Provide licensed or site-specific files that are not committed, such as VASP `POTCAR` files or SIESTA, Quantum Espresso pseudopotentials.
- Use the same MPI stack for Python, DMFTwDFT executables, impurity solvers, Wannier90, and DFT executables.

```{note}
The archived PDF manuals in `/examples/archived_docs` are useful historical references, predating the current DMFTwDFT workflows. The instructions in these manuals are not compatible with the current DMFTwDFT version.
```

A list of current examples is provided below.

```{toctree}
:maxdepth: 2

vasp
siesta
qe
library_mode
```
