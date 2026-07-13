# SrVO3

Source directory: `examples/SrVO3_vasp`

This example is a non-charge-self-consistent SrVO$_3$ DFT+DMFT setup using VASP and a V-$d$ $+$ O-$p$ Wannier subspace.

Included files,

- `input.toml`
- `para_com.dat`
- `INCAR`
- `KPOINTS`
- `POSCAR`

See {doc}`vasp` for general VASP setup requirements, including `POTCAR`, `path_bin`, MPI launcher, and executable setup.

Key settings in `input.toml`:

- `Niter = 1`, so this is a non-charge-self-consistent DMFT run.
- `Nit = 2`, a short DMFT loop intended as an example starting point.
- `n_tot = 19`, for the SrVO$_3$ V-$d$ and O-$p$ Wannier subspace.
- `cor_at = [["V1"]]`, with V-$d$ orbitals treated as correlated.
- `U = [5.0]` and `J = [1.0]`.
- `ewin = [-8, 8]`, relative to the DFT Fermi level.

Run from a copied and edited example directory,

```bash
DMFT.py dmft --dft vasp -v
```

Inspect `DMFT/INFO_ITER` for convergence. After the DMFT run completes, run post-processing from inside `DMFT`,

```bash
postDMFT.py ac --average 2
postDMFT.py dos
postDMFT.py bands --plot-plain --omega-points 1000 --band-k-points 1000 --normalize
```
