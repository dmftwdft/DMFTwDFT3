# DMFTwDFT3 Documentation

DMFTwDFT3 is an open-source, user-friendly framework to calculate properties of strongly correlated materials (SCM) using DFT+DMFT (Dynamical Mean Field Theory) with a variety of different DFT codes. It currently supports VASP, Siesta, and Quantum Espresso.

```{note}
DMFTwDFT3 brings major updates to its Python-2 predecessor, [DMFTwDFT](https://github.com/dmftwdft/DMFTwDFT), with a focus on supporting modern compute architectures including a Python-3 ecosystem, Intel oneAPI LLVM compilers, and MacOS compatibility. Hereafter, DMFTwDFT3 will be referred to as DMFTwDFT for brevity.
```

## Strongly Correlated Materials and DMFT

Electronic correlations in materials give rise to a wide range of emergent phenomena through the intricate interplay among electron spin, charge, orbital degrees of freedom, and lattice distortions. In systems containing localized $d$ or $f$ electrons, such as transition-metal and rare-earth compounds, strong electron-electron interactions lead to remarkable properties including magnetism, high-temperature superconductivity, colossal magnetoresistance, and metal-insulator transitions.

While Density Functional Theory (DFT) has been extraordinarily successful in describing the electronic structure of weakly correlated materials, its static mean-field treatment of electron interactions often fails to capture the physics of strongly correlated materials. In particular, the localized nature of $d$ and $f$ orbitals results in significant many-body effects that are inadequately described by conventional exchange-correlation functionals.

Dynamical Mean-Field Theory (DMFT) has emerged as one of the most successful approaches for treating strong electronic correlations beyond the DFT framework (see [Georges et al., Rev. Mod. Phys. 68, 13 (1996)](https://doi.org/10.1103/RevModPhys.68.13) and [Kotliar et al., Rev. Mod. Phys. 78, 865 (2006)](https://doi.org/10.1103/RevModPhys.78.865)). By incorporating dynamical local correlations through a many-body Green's function formalism, DMFT captures both the itinerant and localized character of electrons.

In DMFT, the lattice problem is mapped onto a self-consistent interacting impurity model (Anderson impurity model), which is solved numerically using advanced impurity solvers such as Continuous-Time Quantum Monte Carlo (CTQMC; see [Haule, Phys. Rev. B 75, 155113 (2007)](https://doi.org/10.1103/PhysRevB.75.155113)). This framework enables an accurate description of many-body fluctuations that are absent in static mean-field approaches.

The combination of DFT and DMFT provides a powerful first-principles methodology for studying strongly correlated materials. In a typical DFT+DMFT workflow, the DFT Kohn-Sham states are projected onto a correlated subspace, often represented using Maximally Localized Wannier Functions (MLWFs; see [Pizzi et al., J. Phys.: Condens. Matter 32, 165902 (2020)](https://doi.org/10.1088/1361-648X/ab51ff)). The resulting low-energy Hamiltonian serves as the basis for the DMFT calculations, where local electronic interactions are treated explicitly. In the DMFT cycle, the impurity problem is solved self-consistently, yielding a frequency-dependent self-energy that captures the many-body effects. This converged DMFT self-energy and density matrix are then fed back into the DFT calculation, and the process is iterated until full charge self-consistency is achieved.

The framework enables the characterization of both weakly and strongly correlated materials through a fully charge-self-consistent DFT+DMFT implementation. In addition, DMFTwDFT provides a library mode for computing the DMFT density matrix, allowing seamless integration with external DFT packages and facilitating the incorporation of charge-self-consistent DFT+DMFT capabilities into existing electronic-structure codes.

```{figure} _static/images/steps.png
:alt: DFT+DMFT workflow
:align: center

Flow diagram of a charge self-consistent DFT+DMFT calculation implemented using the MLWF basis set. Ref: [Park *et al.* Phys. Rev. B 90, 235103 (2014)].
```

## Why DMFTwDFT?

DMFTwDFT offers the following,

1. Conveniently interfaces with multiple DFT codes through the MLWF `wannier90` library.

2. A flexible Python-based interface reduces the amount of user experience and parameter tuning required to perform DFT+DMFT calculations of strongly correlated materials.

3. The implementation has been tested with density of states and band structure calculations for correlated materials including $LaNiO_{3}$, $SrVO_{3}$, and $NiO$.

4. The library mode links the module for computing a DMFT density matrix and updating a charge density within DFT loops without significant DFT source-code changes to enable full-charge self-consistent DFT+DMFT calculations.

DMFTwDFT consists of two main scripts to perform DFT+DMFT calculations:

- `DMFT.py`: performs DFT and DMFT calculations.
- `postDMFT.py`: performs post-processing including analytic continuation, density of states, and band structures.

The `utilities` directory contains optional helper scripts for plotting and analysis.

```{toctree}
:hidden:
:maxdepth: 1
:caption: Contents

installation
workflow
examples/index
utilities
troubleshooting
library
developers
cite
```
