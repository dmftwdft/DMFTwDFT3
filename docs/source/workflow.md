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
| `noms` | Number of Matsubara frequencies for k-sum |
| `dc_type` | Double-counting correction type. See section *"2.4. Total energy and double counting correction"* in the publication for more details. Default: 1 |
| `mu_iter` | Steps for the chemical potential convergence |
| `Nd_qmc` | Default: 0  [0: Use Nd_latt, 1: Use Nd_imp] |
| `sig_tol` | Tolerance for self-energy convergence to end calculation. Default: 1E$^{-03}$ |
| `kmesh_tol` | Tolerance for k-mesh convergence. Default: 1E$^{-07}$ |

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
mpirun -n 16
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

A typical `INFO_ITER` block has the form,

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
postDMFT.py bands --plot-plain --auto-k-path
postDMFT.py bands --plot-partial --wannier-orbitals 2 3 5
postDMFT.py bands --spin-polarized
postDMFT.py bands --compare-dft
```

### Choosing the k-path

The band-structure k-path can be set in three ways.

By default, `postDMFT.py bands` uses a simple-cubic path, $\Gamma$-$X$-$M$-$\Gamma$-$R$, which is appropriate for the SrVO$_3$ examples and little else.

For any other structure, give the path explicitly. `--k-point-list` takes one high-symmetry point per flag occurrence, and `--k-point-names` takes the matching labels in the same order,

```bash
postDMFT.py bands --plot-plain \
    --k-point-list 0 0 0 --k-point-list 0.5 0 0.5 --k-point-list 0.375 0.375 0.75 \
    --k-point-names '$\Gamma$' '$X$' '$K$'
```

Repeat `--k-point-list` once per point, with three fractional coordinates each. `--k-point-names` must have exactly one entry per point, otherwise the run stops with an error rather than producing a mislabelled axis.

Alternatively, `--auto-k-path` reads the path from a VASP line-mode `KPOINTS` file in the `DMFT` directory,

```bash
postDMFT.py bands --plot-plain --auto-k-path
```

The `KPOINTS` file must be in line mode, with the number of points per segment on the second line, the `Reciprocal` keyword, and a `!` label on every k-point line,

```text
k-points along high symmetry lines
40
Line-mode
Reciprocal
   0.0  0.0  0.0 ! GAMMA
   0.5  0.0  0.0 ! X

   0.5  0.0  0.0 ! X
   0.5  0.5  0.0 ! M
```

`GAMMA`, `G`, `GM`, and a literal `Γ` are all rendered as $\Gamma$. Other labels are passed through as LaTeX, so a subscripted point is written `X_1`. Cartesian line mode is not supported. Repeating a segment endpoint with a different label produces a discontinuous path, which is drawn with a break in the axis.

```{note}
`--band-k-points` is a starting value. If the requested number of points cannot be distributed over the path, it is incremented until it can, and the value actually used is printed and recorded in `bands/ksum.input`. This determines the number of blocks in `bands/Gk.out`.
```

### Comparing with a DFT Band Structure

`--compare-dft` overlays the DFT bands on the DMFT spectral function. It works with `--plot-plain`, `--plot-partial`, and the spin-polarized options.

The DMFT run does not produce the files this needs. They come from a separate VASP band-structure calculation,

| File | Purpose | Flag |
| --- | --- | --- |
| `KPOINTS` | line-mode path, supplies the k-path and tick labels | `--kpoints` |
| `EIGENVAL` | DFT eigenvalues along that path | `--eigenval` |
| `OUTCAR` | Fermi energy used to shift the DFT bands | `--outcar` |

Each flag defaults to that file name in the current directory, so copying all three into `DMFT` works. Passing paths instead avoids the copy and, more usefully, avoids a name collision: charge self-consistent runs leave their own `OUTCAR` in the `DMFT` directory, and the DFT band run's `OUTCAR` must not overwrite it.

If any of the three is missing, the run stops immediately. This matters because `EIGENVAL` and `OUTCAR` are not read until after the spectral function has been computed, so an unchecked typo would waste the whole calculation.

`--compare-dft` implies `--auto-k-path`. The path is always taken from the `KPOINTS` file, so that the DMFT and DFT bands share an axis. Combining it with `--k-point-list` or `--k-point-names` is rejected rather than silently ignored.

```{important}
Point `--outcar` at the **self-consistent** `OUTCAR`, meaning the one from the run that produced the `CHGCAR` reused by the `ICHARG=11` calculation. That run sets the absolute energy zero of the eigenvalues in `EIGENVAL`, so only its Fermi energy puts the DFT bands on the same scale as the DMFT spectral function.

The `OUTCAR` written by the line-mode run itself reports a Fermi energy too, but it is computed from a one-dimensional path through the Brillouin zone rather than a proper sampling of it, and is not meaningful. Using it shifts the DFT bands rigidly, typically by several tenths of an eV.

The check is easy to make by eye. Uncorrelated bands well away from the Fermi level, the O $p$ manifold in SrVO$_3$, must lie on top of the corresponding spectral weight. If every DFT band is displaced by the same amount, the Fermi energy is wrong.
```

A typical sequence is a self-consistent run, a non-self-consistent run along the k-path with `ICHARG=11` reusing the converged `CHGCAR`, and then post-processing,

```bash
# DFT band structure, in a separate directory.
# CHGCAR and OUTCAR come from the self-consistent run, so they share an energy zero.
mkdir -p DFT && cp CHGCAR INCAR POSCAR POTCAR DFT/
cp OUTCAR DFT/OUTCAR.scf
cd DFT
cp ../KPOINTS.nscf KPOINTS
sed -i -e 's/.*ICHARG.*/ICHARG=11/g' INCAR
sed -i -e 's/.*LWANNIER.*/LWANNIER=.FALSE./g' INCAR
mpirun -n $SLURM_NTASKS vasp_std > vasp.log 2> vasp.error
cd ..

# post-processing, reading the DFT files in place
cd DMFT
postDMFT.py bands --plot-plain --compare-dft \
    --kpoints ../DFT/KPOINTS --eigenval ../DFT/EIGENVAL --outcar ../DFT/OUTCAR.scf \
    --omega-points 1000 --band-k-points 1000 --normalize
```

Turning off `LWANNIER` for the band run matters. The Wannier projection is only meaningful on a uniform k-mesh, and the line-mode run would otherwise overwrite the Wannier files the DMFT run depends on.

```{note}
This comparison reads VASP-format files only. For SIESTA and Quantum Espresso workflows, there is no built-in equivalent, so either convert your DFT band output to `EIGENVAL` format or plot the DFT bands separately from `bands/Gk.out` as described in {ref}`post-processing-data-files`.
```

### Projected Bands

`--plot-partial` projects the spectral function onto selected Wannier orbitals,

```bash
postDMFT.py bands --plot-partial --wannier-orbitals 2 3 5
```

`--wannier-orbitals` takes 1-based indices into the Wannier orbital ordering described below.

(wannier-orbital-order)=

### Wannier Orbital Order

One ordering is used throughout the post-processing outputs. It is the basis order of the Wannier Hamiltonian, and it is fixed by the projection block that `DMFT.py` writes into `wannier90.win`,

```text
begin projections
V:d
O:p
end projections
```

The order is built up in three nested levels,

1. the entries of `atomnames` in `input.toml`, in the order listed there,
2. within a species, its atoms in the order they appear in the structure file,
3. within an atom, the $2l+1$ orbitals in Wannier90's $m_r$ order.

The projection block names only the species and the angular momentum, so the third level has to be read off Wannier90's convention,

| $l$ | $m_r$ order |
| --- | --- |
| `s` | $s$ |
| `p` | $p_z$, $p_x$, $p_y$ |
| `d` | $d_{z^2}$, $d_{xz}$, $d_{yz}$, $d_{x^2-y^2}$, $d_{xy}$ |
| `f` | $f_{z^3}$, $f_{xz^2}$, $f_{yz^2}$, $f_{z(x^2-y^2)}$, $f_{xyz}$, $f_{x(x^2-3y^2)}$, $f_{y(3x^2-y^2)}$ |

For SrVO$_3$, with `atomnames = ["V", "O"]` and `orbs = ["d", "p"]`, this gives 14 Wannier functions,

| Index | Orbital |
| --- | --- |
| 1-5 | V $d_{z^2}$, $d_{xz}$, $d_{yz}$, $d_{x^2-y^2}$, $d_{xy}$ |
| 6-8 | O(1) $p_z$, $p_x$, $p_y$ |
| 9-11 | O(2) $p_z$, $p_x$, $p_y$ |
| 12-14 | O(3) $p_z$, $p_x$, $p_y$ |

so the $t_{2g}$ manifold is `--wannier-orbitals 2 3 5` and the $e_g$ manifold is `--wannier-orbitals 1 4`.

#### Checking the order for your system

Do not take the convention on trust for a new structure. The `Final State` block of `wannier90.wout` lists the Wannier functions in exactly this order, with their centres and spreads,

```text
 Final State
  WF centre and spread    1  (  1.923260,  1.923260,  1.923260 )     0.58374109
  WF centre and spread    2  (  1.923260,  1.923260,  1.923260 )     0.65265213
  WF centre and spread    3  (  1.923260,  1.923260,  1.923260 )     0.65265215
  WF centre and spread    4  (  1.923260,  1.923260,  1.923260 )     0.58374188
  WF centre and spread    5  (  1.923260,  1.923260,  1.923260 )     0.65265210
  WF centre and spread    6  (  1.923260,  1.923260,  0.000000 )     0.69447337
  ...
```

The centres identify which atom each index belongs to, and the spreads identify the symmetry multiplets within an atom. Here functions 1-5 sit on the V site, and their spreads fall into a twofold group, 1 and 4 at 0.5837, and a threefold group, 2, 3 and 5 at 0.6527. That is the $e_g$ and $t_{2g}$ splitting, confirming the table above from the calculation itself rather than from the convention.

#### Which files use this ordering

```{list-table}
:header-rows: 1

* - Uses Wannier orbital order
  - Uses `cor_orb` group order
* - Column pairs in `dos/G_loc.out`
  - Column pairs in `ac/Sig.out`
* - `orb=` blocks in `bands/Gk.out` from `--plot-partial`
  - Column pairs in `sig.inp` and `sig.inp.*`
* - `--wannier-orbitals`
  - Column pairs in `G_loc.out` and `G_loc.out.*` in the `DMFT` directory
* - `plotDMFTDOS.py`
  - `--cor-orb-index` in `plotDMFT.py` and `Z.py`
```

The two orderings are unrelated and have different lengths. For SrVO$_3$ the Wannier ordering has 14 entries, while `cor_orb` has two, the $e_g$ and $t_{2g}$ groups. Mixing them up is the most common source of wrong custom plots, so check the column count of a file before indexing into it.

The intermediate files `bands/SigMoo_real.out` and `bands/SigMdc.out` use a third layout, the Wannier ordering restricted to the correlated orbitals, which for SrVO$_3$ gives five entries rather than 14 or 2. They are inputs to `dmft_ksum_band` and are not meant for plotting.

For SrVO$_3$, orbitals 1-5 are the V $d$ states and 6-14 the O $p$ states. Wannier90 orders $d$ orbitals as $d_{z^2}$, $d_{xz}$, $d_{yz}$, $d_{x^2-y^2}$, $d_{xy}$, so `--wannier-orbitals 2 3 5` selects the $t_{2g}$ manifold and `--wannier-orbitals 1 4` the $e_g$ manifold. The latter is the default.

`--normalize` rescales the spectral intensity, with `--value-limits` setting the range. This is usually necessary when comparing plots across systems or against DFT bands.

The DMFT band structure is represented by the k-resolved spectral function,

```{math}
A(k, \omega) = \frac{i}{2\pi}\mathrm{Tr}\left[G(k, \omega) - G^{\dagger}(k, \omega)\right]
```

where, the interacting Green's function ($G(k, i\omega_n)$) is constructed from the DFT eigenvalues, the chemical potential, and the DMFT self-energy,

```{math}
G(k, i\omega_n) = \frac{1}{i\omega_n - \epsilon_k + \mu - \Sigma(i\omega_n)}
```

Here, $\omega_n$ is a Matsubara frequency, $\epsilon_k$ is the DFT eigenvalue, $\mu$ is the chemical potential, and ($\Sigma(i\omega_n)$) is the self-energy. After analytic continuation, the real-axis spectral function is plotted by `postDMFT.py bands`.

The DMFT density of states $A(\omega)$ is obtained by summing the spectral function over k-points,

```{math}
A(\omega) = \sum_k A(k, \omega)
```

and is plot with `postDMFT.py dos`.

(post-processing-data-files)=

### Data Files for Custom Plots

Each post-processing step writes a plain-text data file that can be read directly with `numpy.loadtxt` or equivalent if you want to produce your own figures. In all three, the first column is the real frequency $\omega$ in eV, measured relative to the chemical potential, so $\omega = 0$ is the Fermi level.

#### `ac/Sig.out`

The analytically continued self-energy on the real axis, written by `postDMFT.py ac`.

```text
# s_oo= [...]
# Vdc= [...]
omega   Re Sig_1   Im Sig_1   Re Sig_2   Im Sig_2   ...
```

After the two header lines, each row is the frequency followed by a real and imaginary pair for every entry in `cor_orb`, in the order listed in `input.toml`. In the SrVO3 example `cor_orb` groups the $d$ orbitals into $e_g$ and $t_{2g}$, so there are two pairs and five columns in total. This is the `cor_orb` group ordering, not the Wannier orbital ordering; see {ref}`wannier-orbital-order`.

The header lines give the high-frequency limit $\Sigma(\infty)$ (`s_oo`) and the double counting (`Vdc`) for the same components. Only the frequency-dependent part is tabulated, so the self-energy entering the Green's function is $\Sigma(\omega) + \Sigma(\infty) - V_{dc}$.

Use this file for scattering rates from $-\mathrm{Im}\,\Sigma(\omega)$, or for mass enhancement from the slope of $\mathrm{Re}\,\Sigma(\omega)$ near $\omega = 0$.

#### `dos/G_loc.out`

The local Green's function on the real axis, written by `postDMFT.py dos`.

```text
omega   Re G_1   Im G_1   Re G_2   Im G_2   ...
```

There is one real and imaginary pair per Wannier orbital, in the ordering given in {ref}`wannier-orbital-order`, which is the same ordering used by `--wannier-orbitals`. The number of pairs equals the size of the Wannier Hamiltonian. For SrVO3 this is 14 pairs, the five V $d$ orbitals followed by the nine O $p$ orbitals.

The projected density of states for orbital $i$ is,

```{math}
A_i(\omega) = -\frac{1}{\pi}\,\mathrm{Im}\,G_{ii}(\omega)
```

in states/eV/cell. Summing the relevant orbital columns gives a projected or total DOS. This is exactly what `postDMFT.py dos` does to produce `dos/DMFT-PDOS.png`.

The number of rows is set by `--omega-points`.

#### `bands/Gk.out`

The k-resolved Green's function, written by `postDMFT.py bands`. The file is arranged in blocks, one per k-point,

```text
k=   kx   ky   kz
omega   Re G   Im G
omega   Re G   Im G
...
```

The k-point is in fractional coordinates. The number of frequency rows per block is set by `--omega-points` and the number of blocks by `--band-k-points`. Both values are also recorded on the first two lines of `bands/ksum.input`.

There are three columns whatever the size of the system, because $G$ here is the trace over the Wannier basis rather than an orbital-resolved quantity. The `orb=` blocks written by `--plot-partial` are the diagonal elements that sum to it.

The spectral function plotted as the DMFT band structure is,

```{math}
A(k, \omega) = -\frac{1}{\pi}\,\mathrm{Im}\,G(k, \omega)
```

```{warning}
$G(k, \omega)$ is evaluated with a fixed numerical broadening of $\eta = 0.03$ eV, hard-coded in `dmft_ksum_band` and not exposed as an option. Peak widths measured from `Gk.out` therefore include this broadening and are not scattering rates. Take those from $-\mathrm{Im}\,\Sigma(\omega)$ in `ac/Sig.out` instead.
```

To place the blocks on a band-structure axis, use `bands/klist.dat`, which has one row per k-point containing the cumulative distance along the k-path, the three fractional coordinates, and a label on high-symmetry points. Plotting $A(k, \omega)$ against the first column of `klist.dat` and $\omega$ reproduces the `--plot-plain` figure.

```{note}
`--plot-partial` runs `dmft_ksum_partial_band` rather than `dmft_ksum_band` and overwrites `Gk.out` with an orbital-resolved variant, where each k-point block is subdivided by Wannier orbital with an additional `orb=` header line. The `orb=` blocks follow {ref}`wannier-orbital-order`, so every k-point block holds one sub-block per Wannier orbital regardless of which ones `--wannier-orbitals` selected. Copy `Gk.out` elsewhere if you need to keep both forms.
```
