# SrVO3 With VASP

Source directory: `examples/SrVO3_vasp`

This example is a non-charge-self-consistent SrVO3 DFT+DMFT setup using VASP and a V `d` plus O `p` Wannier subspace.

Included files:

- `input.toml`
- `para_com.dat`
- `DFT_mu.out`
- `INCAR`
- `KPOINTS`
- `POSCAR`

Files you must provide or edit:

- `POTCAR`, because VASP pseudopotentials are not distributed with the repository.
- `path_bin` in `input.toml`.
- `para_com.dat` for your MPI launcher.
- VASP executable setup in your environment or DMFTwDFT `bin` directory.

Key settings in `input.toml`:

- `Niter = 1`, so this is a non-charge-self-consistent DMFT run.
- `Nit = 2`, a short DMFT loop intended as an example starting point.
- `n_tot = 19`, for the SrVO3 V `d` and O `p` Wannier subspace.
- `cor_at = [["V1"]]`, with V `d` orbitals treated as correlated.
- `U = [5.0]` and `J = [1.0]`.
- `ewin = [-8, 8]`, relative to the DFT Fermi level.

Run from a copied and edited example directory:

```bash
DMFT.py -dft vasp -dmft
```

Inspect `DMFT/INFO_ITER` for convergence and `DMFT/G_loc.out`, `DMFT/sig.inp.*`, and impurity directories for the DMFT outputs. After the DMFT run completes, run post-processing from inside `DMFT`:

```bash
postDMFT.py ac -siglistindx 2
postDMFT.py dos -show
```
