# VO2 monolayer (2D)

Source directory: `examples/VO2_monolayer_vasp`

This example is a non-charge-self-consistent DFT+DMFT setup for a two-dimensional
system: a single VO$_2$ plane on a square lattice with 20 Å of vacuum, using a
V-$d$ $+$ O-$p$ Wannier subspace.

Nothing in DMFTwDFT is specific to three dimensions. A monolayer is treated as a
slab in a periodic cell, and the two-dimensional character enters only through
the k-meshes, the smearing, the Wannier construction, and the band path. This
example exists to record those settings in one place, since each of them differs
from the bulk examples for a distinct reason.

The deck is constructed as a two-dimensional counterpart to {doc}`srvo3_vasp`
rather than as a model of any known VO$_2$ phase. Removing the apical oxygens
and the Sr sublattice from bulk SrVO$_3$ leaves a VO$_2$ plane, and the in-plane
lattice constant is held at the bulk SrVO$_3$ value of 3.84652 Å rather than
relaxed, so that the V-O bond length is identical in the two calculations.
Vanadium is V$^{4+}$, $d^1$ in both, the Wannier manifold is V $d$ plus O $p$ in
both, and the interaction parameters `U` and `J`, the inverse temperature
`beta` $= 1/k_BT$, and the double-counting scheme are all unchanged. Both decks
use `U = 5.0` eV, `J = 1.0` eV, and `beta = 30.0` eV$^{-1}$, the last
corresponding to $T \approx 387$ K.
Differences between the two runs are therefore attributable to dimensionality
rather than to chemistry, bond length, or parameters.

Included files,

- `input.toml`
- `para_com.dat`
- `INCAR`
- `KPOINTS`
- `KPOINTS.band`
- `POSCAR`
- `submit.sh`

See {doc}`vasp` for general VASP setup requirements, including `POTCAR`, MPI
launcher, and executable setup. A `POTCAR` for V and O in that order is required
and is not distributed with DMFTwDFT. The deck assumes `V_pv`.

## System

| Quantity | Value |
| --- | --- |
| Cell | $a = b = 3.84652$ Å, $c = 20.0$ Å |
| Atoms | V at $(0,0,\tfrac12)$; O at $(\tfrac12,0,\tfrac12)$ and $(0,\tfrac12,\tfrac12)$ |
| Coordination | Square-planar VO$_4$, aligned with the Cartesian axes |
| Formal valence | V$^{4+}$ ($d^1$), O$^{2-}$ |
| Wannier manifold | 11 orbitals: V $d$ (5) + 2 $\times$ O $p$ (6) |
| Electrons in manifold | 13 = $d^1$ + 2 $\times$ $p^6$ |

The layer is placed at $z = \tfrac12$ so that it sits at the centre of the cell
rather than straddling the periodic boundary.

Removing the apical oxygens of the parent perovskite lowers the site symmetry
from $O_h$ to $D_{4h}$, which splits the $d$ shell into four irreducible
representations. `cor_orb` reflects this decomposition exactly:

<!-- prettier-ignore -->
| Group | Orbitals | Irrep |
| --- | --- | --- |
| 1 | `d_z2` | $a_{1g}$ |
| 2 | `d_x2y2` | $b_{1g}$ |
| 3 | `d_xy` | $b_{2g}$ |
| 4 | `d_xz`, `d_yz` | $e_g$ |

The bulk $t_{2g}$ triplet is split into `d_xy` and the `d_xz`/`d_yz` pair, and
the lifting of that degeneracy is the physical signature the calculation should
reproduce. All five $d$ orbitals appear in `cor_orb`, so the Hartree-Fock path
is not used. Since the square-planar environment is aligned with the Cartesian
axes, `L_rot = [0, 0]` is correct and no local axis rotation is required.

## Two-dimensional settings

These are the parameters that differ from a bulk deck, and the reason for each.

- **`KPOINTS` is `12 12 1`.** A single k-point along the non-periodic direction.
- **`q = [24, 24, 1]`.** The DMFT k-sum mesh. In a non-charge-self-consistent
  run the Hamiltonian is Wannier-interpolated onto this mesh directly, so `q` is
  independent of the DFT `KPOINTS` mesh and need not be a multiple of it. A
  single point along $k_z$ is correct for a slab: leaving $q_z$ at the bulk
  value of 24 would sample a dispersionless direction 24 times over, which is
  not wrong, only 24 times more expensive.

  In charge-self-consistent runs driven through the library interface, the mesh
  is instead refined from the DFT k-points using
  `nfine(i) = int(q(i)/mp_grid(i))`. There `q` must be at least as large as the
  DFT mesh componentwise, since a smaller value gives `nfine = 0` and collapses
  that direction silently.
- **`num_iter_win = 0`.** This is the setting most specific to slabs and the one
  most likely to be missed. See below.
- **`ISMEAR = 0`, `SIGMA = 0.05`.** Gaussian smearing rather than the tetrahedron
  method used in the bulk examples. The tetrahedron method is unreliable when
  only one k-point exists along the third direction.
- **`KPOINTS.band`.** The default k-path is simple cubic and includes
  $R = (\tfrac12,\tfrac12,\tfrac12)$, which is meaningless for a slab.

## Wannier functions in a slab cell

With a single k-point along the vacuum direction, the only finite-difference
b-vector available along that direction has $|b| = 2\pi/c$, which for $c = 20$ Å
is small enough that the spread computed along $z$ carries no useful
information. The symptom is unmistakable in `wannier90.wout`: every Wannier
function reports a spread of order 100 Å$^2$ already in the `Initial State`
block, before any minimization, and $\Omega_D$ is three orders of magnitude
larger than $\Omega_I$.

The subspace itself is unaffected, and $\Omega_I$ and $\Omega_{OD}$ remain
small and meaningful. What fails is the spread minimization, which then spends
its iterations moving Wannier centres along a direction in which the objective
function is meaningless. Centres drift away from the atomic plane even though
every atom lies in it.

Setting `num_iter_win = 0` skips the minimization and keeps the projected
Wannier functions, which is the appropriate choice for a slab and is a common
choice for DFT+DMFT generally. Disentanglement is a separate step and is still
performed; `dis_num_iter_win` stays at its default.

## Running

From a copied and edited example directory,

```bash
DMFT.py dmft --dft vasp -v
```

Inspect `DMFT/INFO_ITER` for convergence. After the DMFT run completes, run
post-processing from inside `DMFT`,

```bash
postDMFT.py ac --average 10
postDMFT.py dos
postDMFT.py bands --plot-plain --omega-points 1000 --band-k-points 1000 \
    --normalize --auto-k-path --kpoints ../KPOINTS.band
```

`KPOINTS.band` is kept separate from `KPOINTS`, which holds the
$12 \times 12 \times 1$ SCF mesh. The `--kpoints` flag exists so that neither
has to be copied or renamed. The same file serves as the line-mode `KPOINTS` for
a VASP band-structure run (`ICHARG = 11`, reusing the SCF `CHGCAR`) if a
`--compare-dft` overlay is wanted. In that case pass the SCF `OUTCAR` to
`--outcar`, since the absolute energy zero comes from the run that produced the
charge density.

## What to check

1. **Wannier quality first.** Confirm in `wannier90.wout` that the 11 final
   Wannier centres sit on the V and O sites. A vacuum-localized Wannier function
   is the characteristic failure mode of a slab calculation and invalidates
   everything downstream.
2. **`ewin`.** This is the parameter most likely to need adjustment in 2D. With
   20 Å of vacuum the vacuum level sits a few eV above $E_F$, and free-electron
   slab states form a dense ladder above it. The window `[-7, 7]` is a starting
   point spanning O $2p$ through the V $d$ manifold including the strongly
   antibonding `d_x2y2`; it may reach the onset of those vacuum states. Inspect
   the DFT density of states and adjust. If disentanglement selects vacuum
   states even so, write a `wannier90.win` by hand with `dis_froz_min` and
   `dis_froz_max`, which DMFTwDFT does not write, and pass `--no-win` to
   `DMFT.py` so the file is not regenerated.
3. **Occupancy.** `INFO_ITER` should show `Nd_latt` and `Nd_imp` approaching each
   other. A persistent gap between them points at the Wannier window or at an
   unconverged loop rather than at the impurity solver.
4. **The dimensional signature.** In `ac/Sig.out` the four self-energy groups are
   no longer degenerate as the bulk $t_{2g}$ triplet was. Compare the
   quasiparticle residues against the bulk SrVO$_3$ run with
   `Z.py --average 5 --cor-orb-index 3` and `4`.

## Wannier orbital ordering

For `postDMFT.py bands --plot-partial -w`, the Wannier order follows the
projection block (`V:d` then `O:p`), one-based:

<!-- prettier-ignore -->
| Index | Orbital | Index | Orbital |
| --- | --- | --- | --- |
| 1 | V `d_z2` | 7 | O1 `p_x` |
| 2 | V `d_xz` | 8 | O1 `p_y` |
| 3 | V `d_yz` | 9 | O2 `p_z` |
| 4 | V `d_x2y2` | 10 | O2 `p_x` |
| 5 | V `d_xy` | 11 | O2 `p_y` |
| 6 | O1 `p_z` | | |

The `--cor-orb-index` argument of `plotDMFT.py` and `Z.py` refers to the four
`cor_orb` groups tabulated earlier instead, and is unrelated to this ordering.
