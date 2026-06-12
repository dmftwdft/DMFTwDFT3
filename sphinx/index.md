# DMFTwDFT3 Documentation

DMFTwDFT is an open-source, user-friendly framework to calculate electronic, vibrational and elastic properties in strongly correlated materials (SCM) using beyond-DFT methods such as DFT+U, DFT+Hybrids and DFT+DMFT (Dynamical Mean Field Theory) with a variety of different DFT codes. Currently VASP, Siesta and Quantum Espresso through AiiDA are supported.

## Overview

DMFTwDFT offers the following:

1. DMFT has been one of the most successful methods treating many-body fluctuations by including dynamical but local correlations beyond the static DFT exchange-correlation functional. DMFTwDFT is interfaced with Wannier90 for extension to several DFT codes.
2. The library mode links the module for computing a DMFT density matrix and updating a charge density within DFT loops without significant DFT source-code changes.
3. A flexible Python-based interface reduces the amount of user experience and parameter tuning required to perform DFT+DMFT calculations of strongly correlated materials.
4. The implementation has been tested with density of states and band structure calculations for correlated materials including $LaNiO_{3}$, $SrVO_{3}$, and $NiO$.
5. Future work includes force calculations for phonon calculations in strongly correlated materials and ab-initio Hubbard U calculations using the linear-response approach developed by Cococcioni et al.

DMFTwDFT consists of two main scripts to perform DFT+DMFT calculations:

- `DMFT.py`: performs DFT and DMFT calculations.
- `postDMFT.py`: performs post-processing including analytic continuation, density of states, and band structures.

The `/scripts` directory contains several utility scripts.

```{toctree}
:maxdepth: 2
:caption: Contents

installation
tutorials
library
developers
cite
```

## Indices and Tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
