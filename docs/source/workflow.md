# Workflow

DMFTwDFT combines a DFT calculation, a Wannier90 projection, and a DMFT self-consistency loop. The main DMFT executable computes the local Green's function `G_loc.out` and hybridization function `Delta.out` from the current self-energy `sig.inp`. The impurity solver then updates the self-energy, and the process repeats until the lattice and impurity quantities converge.

The calculation steps are,

1. Configure `input.toml` for DFT+DMFT parameters, `para_com.dat` for parallelization of DMFT, and optionally `para_com_dft.dat` for parallelization of DFT. The content of both `para_com.dat` and `para_com_dft.dat` is `mpirun -n <N>`, where `<N>` is the number of MPI processes.
2. Within `input.toml`, define a Wannier subspace for the correlated orbitals.
3. Run `DMFT.py` to launch the DFT+DMFT calculation.
4. Inspect `INFO_ITER` for convergence. Based on the `sig_tol` value in `input.toml` (default `sig_tol` is 1E$^{-03}$ eV), the DMFT loop will stop when the required self-energy convergence is reached.
5. Run `postDMFT.py` for analytic continuation, density of states, and band structures.
6. Optionally, run utility scripts for further analysis.

## Wannier Subspace

Choose the Wannier energy window from the DFT band structure, usually with the help of orbital-projected bands. The window should contain the correlated orbitals and any strongly hybridized states needed to represent the low-energy subspace.

In `input.toml`, the window is set by `ewin` relative to the DFT Fermi energy. For example, the LaNiO$_3$ VASP example uses:

```toml
ewin = [-8, 3.1]
```

If the DFT Fermi level is 7.6986 eV and the desired absolute window is approximately -8 eV to 3 eV relative to the Fermi level, the `wannier90.win` disentanglement limits are shifted by the Fermi level:

```text
dis_win_min = -0.3014
dis_win_max = 10.6986
num_wann = 28
```

For transition-metal oxides, the projection often includes metal $d$ orbitals and oxygen $p$ orbitals. In the LaNiO$_3$ example, 2 Ni atoms contribute 10 $d$ Wannier functions and 6 O atoms contribute 18 $p$ Wannier functions, for `num_wann = 28`.

For low-symmetry octahedral environments, rotate local $d$ axes when needed with the `L_rot` parameter to reduce off-diagonal Hamiltonian terms in the correlated basis. This utilizes the `generate_win.py` helper functions to generate local projection axes.

## Input Parameters

Most calculation parameters live under the `[p]` section in `input.toml`. Please refer to the DMFTwDFT publication ([Singh, V., Herath, U., _et al._ Comput. Phys. Commun. **261**, 107778 (2021)](https://doi.org/10.1016/j.cpc.2020.107778)) for further details and physical context of the parameters. The following table summarizes the most important parameters for a DFT+DMFT calculation.

<!-- prettier-ignore -->
| Parameter | Definition |
| --- | --- |
| `Niter` | Number of full DFT+DMFT iterations. `Niter = 1` is a non-charge-self-consistent DFT+DMFT calculation (one-shot DMFT). Values >1 request charge-self-consistent loops when the DFT interface supports them. |
| `Nit` | Number of DMFT self-consistency iterations per outer loop. |
| `Ndft` | Number of DFT iterations in a charge-self-consistent outer loop. |
| `n_tot` | Total number of electrons in the Wannier subspace. E.g., for LaNiO$_3$ with 2 Ni ions and 6 O ions, `n_tot` =  2 $\times$ 7 Ni $d$ electrons + 6 $\times$ 6 O $p$ electrons =  50 electrons|
| `nf` | Nominal occupancy of $d$ or $f$ electrons in a correlated atom. Used for the initial guess of self-energy. Initialize it as the DFT occupancy of the correlated atom or the nominal electron number. |
| `nspin` | Number of DMFT spin channels. Use `2` for spin-polarized DMFT calculations. |
| `atomnames` | Atom species used to construct the Wannier basis. |
| `orbs` | Orbital channels used to construct the Wannier basis. |
| `L_rot` | Whether to rotate local projection axes for each atom/orbital channel. Use `1` for rotated local axes and `0` otherwise. |
| `cor_at` | Correlated atoms. Symmetry-equivalent atoms can be grouped together. |
| `cor_orb` | Correlated orbitals on each correlated atom. Orbitals listed here are treated by DMFT; other orbitals in the Wannier subspace are treated outside the impurity problem. |
| `U` | Hubbard interaction for each correlated atom group. |
| `J` | Hund coupling for each correlated atom group. |
| `alpha` | Double-counting correction parameter. `alpha = 0` corresponds to the conventional fully localized limit. |
| `mix_sig` | Mixing parameter between previous and current self-energies. |
| `q` | Dense k-point mesh used for the DMFT Wannier k-sum. This is often chosen larger than the DFT k-mesh because the Wannier interpolation is cheaper than the DFT calculation. |
| `ewin` | Wannier projection energy window relative to the DFT Fermi energy. |
| `path_bin` | Path to the DMFTwDFT `bin` directory. |
| `noms` | Number of Matsubara frequencies for k-sum |
| `dc_type` | Double-counting correction type. See section *"2.4. Total energy and double counting correction"* in the publication for more details. Default: 1 |
| `mu_iter` | Steps for the chemical potential convergence |
| `Nd_qmc` | Default: 0  [0: Use Nd_latt, 1: Use Nd_imp] |
| `sig_tol` | Tolerance for self-energy convergence to end calculation. Default: 1E$^{-03}$ |
| `kmesh_tol` | Tolerance for k-mesh convergence. Default: 1E$^{-03}$ |

The `[pC]` table contains impurity-solver settings and the `[pD]` table contains CIX/atomic solver parameters passed to the impurity setup. For these solver-specific parameters, refer to the CTQMC documentation on the [eDMFT website](http://hauleweb.rutgers.edu/tutorials/Overview.html).

## Running a Calculation

Run `DMFT.py` from a calculation directory containing `input.toml`, `para_com.dat`, and the DFT inputs required by the selected backend. The `-h` or `--help` option lists a comprehensive set of available input arguments for `DMFT.py`. The main subcommands are `ac`, `dos`, and `bands`. The `--help` option for each subcommand lists the available options.

Examples,

```bash
DMFT.py dmft --dft vasp
DMFT.py dmft --dft siesta --structure-name SrVO3
DMFT.py dmft --dft qe --structure-name SrVO3
DMFT.py dmft --dft qe --aiida --verbose
```

Use the `hf` subcommand instead of `dmft` to run the Hartree-Fock path for the correlated orbitals. Use `--restart` to restart from the beginning. For SIESTA and QE, `--structure-name` should match the seed name used by files such as `<seed>.fdf`, `<seed>.scf.in`, and Wannier90 outputs.

`para_com.dat` contains the MPI command for DMFTwDFT and the impurity solver, for example,

```text
mpirun -np 16
```

If the DFT executable needs a different MPI command, place it in `para_com_dft.dat`; otherwise DMFTwDFT reuses `para_com.dat`.

A collection of example workflows for VASP, SIESTA, and Quantum Espresso is provided in {doc}`examples/index`.

## Output Files

The main runtime files are written inside the generated `DMFT` or `HF` directory.

<!-- prettier-ignore -->
| File | Description |
| --- | --- |
| `INFO_ITER` | Main convergence table. Columns include DFT/DMFT iterations, lattice/impurity occupancy, lattice/impurity self-energy, total-energy estimates, and charge difference for charge-self-consistent runs. See {ref}`Monitoring Progress <monitoring-progress>`. |
| `INFO_KSUM` | DMFT k-sum information such as chemical potential, total electron count, occupancies, kinetic energy, and self-energy high-frequency terms. |
| `INFO_DM` | Occupancy matrix information. |
| `INFO_ENERGY` | DFT energy and DMFT energy corrections. |
| `INFO_TIME` | Timing information. |
| `INFO_DFT_loop` | DFT-loop summary for charge-self-consistent calculations. |
| `G_loc.out` | Local Green's function from the lattice k-sum. |
| `Delta.out` | Hybridization function. |
| `sig.inp` | Current self-energy on the imaginary axis. Archived as `sig.inp.<outer>.<dmft>` for each iteration. |

(monitoring-progress)=

## Monitoring Progress

During a run, `INFO_ITER` is usually the first file to inspect. It records the total or outer DFT+DMFT iteration, the inner DMFT iteration, lattice and impurity occupancies, self-energy and double-counting related quantities, two total-energy estimates, and the charge difference between consecutive charge updates.

A typical `INFO_ITER` block has the form:

```text
DFT_iter DMFT_iter Nd_latt Nd_imp (Sigoo-Vdc)_latt (Sigoo-Vdc)_imp TOT_E(Tr(SigG)) TOT_E(EPOT_imp) charge_diff
1 10  7.798655 7.797084       1.669025       1.644641       -68.440528    -68.086689 0.000000
1 11  7.798642 7.797683       1.668703       1.644087       -68.444524    -68.088970 0.000000
1 12  7.798855 7.796977       1.669338       1.644704       -68.446219    -68.090861 0.000000
```

The columns are (from left to right),

<!-- prettier-ignore -->
| Column | Definition |
| --- | --- |
| `DFT_iter` | Total DFT+DMFT iteration step. For non-charge-self-consistent calculations this stays at `1`; for charge-self-consistent calculations it increases with each outer charge loop. |
| `DMFT_iter` | Inner DMFT iteration step within the current outer DFT+DMFT iteration. For example, `1 10` means outer iteration 1 and DMFT iteration 10. |
| `Nd_latt` | Correlated-shell occupancy from the local lattice calculation, i.e. from the lattice Green's function. In the examples this is the lattice $d$ occupancy. |
| `Nd_imp` | Correlated-shell occupancy from the CTQMC impurity calculation. A converged DMFT loop should make this impurity occupancy equal, within tolerance, to `Nd_latt`. |
| `(Sigoo-Vdc)_latt` | Lattice value of the high-frequency self-energy with double-counting correction |
| `(Sigoo-Vdc)_imp` | Impurity/CTQMC value of high-frequency self-energy with double-counting correction. A converged DMFT loop should make this impurity value consistent with `(Sigoo-Vdc)_latt`. |
| `TOT_E(Tr(SigG))` | Total energy computed with the Migdal-Galitskii method using the `Tr(Sigma G)` interaction-energy contribution. |
| `TOT_E(EPOT_imp)` | Total energy computed using the CTQMC-sampled impurity potential energy. |
| `charge_diff` | Charge-density difference between two consecutive outer steps. For non-charge-self-consistent calculations this is `0`; for charge-self-consistent calculations this is the value to monitor for charge convergence. |

To judge convergence, compare lattice and impurity quantities in `INFO_ITER`. In a converged DMFT loop, `Nd_latt` and `Nd_imp` should approach each other, and the lattice and impurity `(Sigoo - Vdc)` values should stabilize.

Use `INFO_TIME` to identify expensive stages or stalled calculations. Use `INFO_KSUM` to inspect the lattice k-sum, including chemical potential, total electron count, occupancies, kinetic energy, and self-energy high-frequency terms. Use `INFO_ENERGY` when comparing total-energy estimates across iterations.

## Post-Processing

Run `postDMFT.py` inside the completed `DMFT` or `HF` directory. The `-h` or `--help` option lists a comprehensive set of available input arguments for each subcommand. The main subcommands are `ac`, `dos`, and `bands`. The `--help` option for each subcommand lists the available options.

Analytic continuation averages the last self-energy files and writes `ac/Sig.out` on the real axis,

```bash
postDMFT.py ac --average 4
```

Density-of-states calculations use the real-axis self-energy and write outputs under `dos`,

```bash
postDMFT.py dos
```

Band-structure calculations write outputs under `bands`,

```bash
postDMFT.py bands --plot-plain
postDMFT.py bands --plot-partial --wannier-orbitals 4 5 6
postDMFT.py bands --spin-polarized
postDMFT.py bands --compare-dft
```

For projected bands, `--wannier-orbitals` uses 1-based Wannier orbital indices. The ordering follows the atom order in the structure and the Wannier orbital order.

The DMFT band structure is represented by the k-resolved spectral function,

```{math}
A(k, \omega) = \frac{i}{2\pi}\mathrm{Tr}\left[G(k, \omega) - G^{\dagger}(k, \omega)\right]
```

where the interacting Green's function is constructed from the DFT/Wannier eigenvalues, the chemical potential, and the DMFT self-energy,

```{math}
G(k, i\omega_n) = \frac{1}{i\omega_n - \epsilon_k + \mu - \Sigma(i\omega_n)}
```

Here `omega_n` is a Matsubara frequency, `epsilon_k` is the DFT/Wannier eigenvalue, `mu` is the chemical potential, and `Sigma` is the self-energy ($\Sigma(i\omega_n)$). After analytic continuation, the real-axis spectral function is plotted by `postDMFT.py bands`.

The DMFT density of states is obtained by summing the spectral function over k-points,

```{math}
A(\omega) = \sum_k A(k, \omega)
```
