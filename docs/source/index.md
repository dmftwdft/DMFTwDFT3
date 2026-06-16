# DMFTwDFT3 Documentation

DMFTwDFT is an open-source, user-friendly framework to calculate properties of strongly correlated materials (SCM) using DFT+DMFT (Dynamical Mean Field Theory) with a variety of different DFT codes. Currently supports VASP, Siesta, and Quantum Espresso.

## Overview

DMFTwDFT offers the following:

1. DMFT has been one of the most successful methods treating many-body fluctuations by including dynamical, local correlations beyond the static DFT exchange-correlation functional. DMFTwDFT is interfaced with Wannier90 for extension to several DFT codes.

2. A flexible Python-based interface reduces the amount of user experience and parameter tuning required to perform DFT+DMFT calculations of strongly correlated materials.

3. The implementation has been tested with density of states and band structure calculations for correlated materials including $LaNiO_{3}$, $SrVO_{3}$, and $NiO$.

4. The library mode links the module for computing a DMFT density matrix and updating a charge density within DFT loops without significant DFT source-code changes to enable full-charge self-consistent DFT+DMFT calculations.

DMFTwDFT consists of two main scripts to perform DFT+DMFT calculations:

- `DMFT.py`: performs DFT and DMFT calculations.
- `postDMFT.py`: performs post-processing including analytic continuation, density of states, and band structures.

The `/scripts` directory contains several utility scripts.

```{toctree}
:maxdepth: 2
:caption: Contents

installation
tutorials
workflow
troubleshooting
library
developers
cite
```
