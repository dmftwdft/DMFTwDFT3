# Workflow

DMFTwDFT combines a DFT calculation, a Wannier90 projection, and a DMFT impurity loop. The main DMFT executable computes the local Green's function `G_loc.out` and hybridization functions `Delta*.inp` from the current self-energy `sig.inp`. The impurity solver then updates the self-energy, and the process repeats until the lattice and impurity quantities converge.

The normal calculation stages are,

1. Configure `input.toml` for DFT+DMFT parameters, `para_com.dat` for parallelization of DMFT, and optionally `para_com_dft.dat` for parallelization of DFT.
2. Within `input.toml`, define a Wannier subspace for the correlated orbitals.
3. Run `DMFT.py` to prepare DFT/Wannier inputs and launch the DMFT or Hartree-Fock loop.
4. Inspect `INFO_ITER` for convergence. Based on the `sig_tol` value in `input.toml`, the DMFT loop will stop when the required self-energy convergence is reached.
5. Run `postDMFT.py` for analytic continuation, density of states, and band structures.

## Wannier Subspace

Choose the Wannier energy window from the DFT band structure, usually with the help of orbital-projected bands. The window should contain the correlated orbitals and any strongly hybridized states needed to represent the low-energy subspace.

In `input.toml`, the window is set by `ewin` relative to the DFT Fermi energy. For example, the LaNiO$_3$ VASP example uses:

```toml
ewin = [-8, 3.1]
```

The older PDF tutorial gives the corresponding Wannier90 idea explicitly. If the DFT Fermi level is 7.6986 eV and the desired absolute window is approximately -8 eV to 3 eV relative to the Fermi level, the `wannier90.win` disentanglement limits are shifted by the Fermi level:

```text
dis_win_min = -0.3014
dis_win_max = 10.6986
num_wann = 28
```

For transition-metal oxides, the projection often includes metal `d` orbitals and oxygen `p` orbitals. In the LaNiO3 example, 2 Ni atoms contribute 10 `d` Wannier functions and 6 O atoms contribute 18 `p` Wannier functions, for `num_wann = 28`.

For low-symmetry octahedral environments, rotate local `d` axes when needed to reduce off-diagonal Hamiltonian terms in the correlated basis. The current input uses `L_rot`; the helper `generate_win.py` can be used when local projection axes need to be generated.

## Important Input Parameters

Most calculation settings live under the `[p]` table in `input.toml`.

`Niter`
: Number of outer DFT+DMFT iterations. `Niter = 1` is a non-charge-self-consistent DFT+DMFT calculation. Larger values request charge-self-consistent loops when the DFT interface supports them.

`Nit`
: Number of DMFT self-consistency iterations per outer loop.

`Ndft`
: Number of DFT iterations in a charge-self-consistent outer loop.

`n_tot`
: Total number of electrons in the Wannier subspace. For LaNiO3 with 2 Ni ions and 6 O ions, a common count is 2 x 7 Ni `d` electrons plus 6 x 6 O `p` electrons, giving 50.

`nf`
: Target or initial correlated-shell occupancy. This can be a nominal value or a DFT-estimated occupancy.

`nspin`
: Number of DMFT spin channels. Use `2` for spin-polarized DMFT calculations.

`atomnames` and `orbs`
: Atom species and orbital channels used to construct the Wannier basis.

`L_rot`
: Whether to rotate local projection axes for each atom/orbital channel. Use `1` for rotated local axes and `0` otherwise.

`cor_at`
: Correlated atoms. Symmetry-equivalent atoms can be grouped together.

`cor_orb`
: Correlated orbitals on each correlated atom. Orbitals listed here are treated by DMFT; other orbitals in the Wannier subspace are treated outside the impurity problem.

`U` and `J`
: Hubbard interaction and Hund coupling for each correlated atom group.

`alpha`
: Double-counting correction parameter. The PDF manuals describe `alpha = 0` as the conventional fully localized limit; current examples often use nonzero values selected for the material.

`mix_sig`
: Mixing parameter between previous and current self-energies.

`q`
: Dense k-point mesh used for the DMFT Wannier k-sum. This is often chosen larger than the DFT k-mesh because the Wannier interpolation is cheaper than the DFT calculation.

`ewin`
: Wannier projection energy window relative to the DFT Fermi energy.

`path_bin`
: Path to the DMFTwDFT `bin` directory. Set this to your local checkout; do not copy the absolute paths from bundled examples.

The `[pC]` table contains impurity-solver settings such as inverse temperature `beta`, Monte Carlo steps `M`, Matsubara sampling `nom`, warmup, and measurement parameters. The `[pD]` table contains CIX/atomic solver parameters passed to the impurity setup.

## Running A Calculation

Run `DMFT.py` from a calculation directory containing `input.toml`, `para_com.dat`, and the DFT inputs or outputs required by the selected backend.

Examples:

```bash
DMFT.py dmft --dft vasp
DMFT.py dmft --dft siesta --structure-name SrVO3
DMFT.py dmft --dft qe --structure-name SrVO3
DMFT.py dmft --dft qe --aiida --verbose
```

Use the `hf` subcommand instead of `dmft` to run the Hartree-Fock path for the correlated orbitals. Use `--restart` to restart from the beginning. For SIESTA and QE, `--structure-name` should match the seed name used by files such as `<seed>.fdf`, `<seed>.scf.in`, and Wannier90 outputs.

`para_com.dat` contains the MPI command for DMFTwDFT and the impurity solver, for example:

```text
mpirun -np 16
```

If the DFT executable needs a different MPI command, place it in `para_com_dft.dat`; otherwise DMFTwDFT reuses `para_com.dat`.

## SIESTA Notes

For SIESTA calculations, the calculation directory should contain `input.toml`, `para_com.dat`, optional `para_com_dft.dat`, `<seed>.fdf`, pseudopotential files such as `.psf`, and optionally an initial `DFT_mu.out`. For the bundled SrVO3 example, the seed is `SrVO3`, so the main SIESTA input is `SrVO3.fdf` and the command uses `--structure-name SrVO3`.

The SIESTA `.fdf` file must request the Wannier90 files that DMFTwDFT needs. The historical SIESTA PDF lists the essential block:

```text
Siesta2Wannier90.WriteMmn .true.
Siesta2Wannier90.WriteAmn .true.
Siesta2Wannier90.WriteEig .true.
Siesta2Wannier90.WriteUnk .false.
Siesta2Wannier90.NumberOfBands 28
```

Adjust `Siesta2Wannier90.NumberOfBands` for the material and energy window. The SrVO3 PDF example used 28 DFT bands and 14 Wannier bands for V `d` and O `p` states.

DMFTwDFT generates the Wannier90 input unless `--no-win` is supplied. For SIESTA workflows, it runs Wannier90 preprocessing to create `<seed>.nnkp`, runs SIESTA, then runs Wannier90 and the DMFT loop.

The `--lowdin` flag is available for the SIESTA Lowdin workflow:

```bash
DMFT.py dmft --dft siesta --structure-name SrVO3 --lowdin
```

The SIESTA PDF also describes charge self-consistency. The key idea is the same as the general library-mode formalism in {doc}`library`: replace the ordinary DFT contribution from bands inside the correlated Wannier window with a DMFT occupancy-matrix contribution, while keeping bands outside the window at their DFT occupancy.

The PDF's `subroutine_dmft` test directory describes prototype files named `test_dmft.F90`, `dmft.F90`, and `libdmft.a`. In the current source tree, the library entry points are implemented in `sources/src/dmft_lib.F90`, and the bundled test is under `examples/library_mode_test`.

## Output Files

The main runtime files are written inside the generated `DMFT` or `HF` directory.

`INFO_ITER`
: Main convergence table. Columns include outer iteration, DMFT iteration, lattice occupancy `Nd_latt`, impurity occupancy `Nd_imp`, lattice and impurity `(Sigoo - Vdc)`, two total-energy estimates, and charge difference for charge-self-consistent runs.

`INFO_KSUM`
: DMFT k-sum information such as chemical potential, total electron count, occupancies, kinetic energy, and self-energy high-frequency terms.

`INFO_DM`
: Occupancy matrix information.

`INFO_ENERGY`
: DFT energy and DMFT energy corrections.

`INFO_TIME`
: Timing information.

`INFO_DFT_loop`
: DFT-loop summary for charge-self-consistent calculations.

`G_loc.out`
: Local Green's function from the lattice k-sum.

`Delta*.inp`
: Hybridization functions passed to impurity problems.

`sig.inp` and `sig.inp.<outer>.<dmft>`
: Current and archived self-energy files on the imaginary axis.

To judge convergence, compare lattice and impurity quantities in `INFO_ITER`. In a converged DMFT loop, `Nd_latt` and `Nd_imp` should approach each other, and the lattice and impurity `(Sigoo - Vdc)` values should stabilize. In charge-self-consistent runs, also monitor the final charge-difference column.

## Post-Processing

Run `postDMFT.py` inside the completed `DMFT` or `HF` directory.

Analytic continuation averages the last self-energy files and writes `ac/Sig.out` on the real axis:

```bash
postDMFT.py ac --average 4
```

Density-of-states calculations use the real-axis self-energy and write outputs under `dos`:

```bash
postDMFT.py dos --show
```

Band-structure calculations write outputs under `bands`:

```bash
postDMFT.py bands --plot-plain
postDMFT.py bands --plot-partial --wannier-orbitals 4 5 6
postDMFT.py bands --spin-polarized --show
postDMFT.py bands --compare-dft
```

For projected bands, `--wannier-orbitals` uses 1-based Wannier orbital indices. The ordering follows the atom order in the structure and the Wannier orbital order.

## Legacy PDF Command Mapping

Some commands in the PDF manuals are old names or manual steps that are now wrapped by `DMFT.py` and `postDMFT.py`.

| PDF-era item                                                          | Current usage                                                          |
| --------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `INPUT.py`                                                            | `input.toml`                                                           |
| `Copy-input.py` / `Copy_input.py` for normal setup                    | Usually handled by `DMFT.py`                                           |
| `RUNDMFT.py` as the user-facing entry point                           | Usually launched by `DMFT.py`                                          |
| `INFO-ITER`, `INFO-ENERGY`, `INFO-KSUM`, `INFO-DM`, `INFO-TIME`       | `INFO_ITER`, `INFO_ENERGY`, `INFO_KSUM`, `INFO_DM`, `INFO_TIME`        |
| Manual `sigaver.py`, `maxent_run.py`, `Interpol_sig_real.py` sequence | `postDMFT.py ac`, followed by `postDMFT.py dos` or `postDMFT.py bands` |
| Manual `dmft-dos.x` command                                           | `postDMFT.py dos` runs the DOS workflow                                |
| Manual `dmft_ksum_band` and plotting scripts                          | `postDMFT.py bands` runs the band workflow                             |

The legacy scripts remain useful for debugging individual stages, but the documented workflow should use the current top-level commands first.
