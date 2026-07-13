# LaNiO3

Source directories,

- `examples/LaNiO3_vasp/NCSC`
- `examples/LaNiO3_vasp/CSC`

The non-charge-self-consistent and charge-self-consistent examples use the same Ni-$d$ $+$ O-$p$ Wannier subspace but different loop settings.

Included files in each subdirectory,

- `input.toml`
- `INCAR`
- `KPOINTS`
- `POSCAR`
- `submit.sh`

See {doc}`vasp` for general VASP setup requirements, including `POTCAR`, `path_bin`, MPI launcher, and executable setup.

The non-charge-self-consistent example has,

- `Niter = 1`
- `Nit = 15`
- `n_tot = 50.0`
- `nf = 7.0`
- `L_rot = [1, 0]`, rotating the Ni local axes.
- `cor_at = [["Ni1", "Ni2"]]`
- `ewin = [-8, 3.1]`

The charge-self-consistent example has,

- `Niter = 15`
- `Ndft = 10`
- `Nit = 1`
- The same Ni/O correlated subspace settings as the NCSC case.

Run from a copied and edited `CSC` or `NCSC` directory,

```bash
DMFT.py dmft --dft vasp -v
```

Charge-self-consistent VASP workflows require the VASP-side DMFTwDFT interface described in {doc}`../installation` and {doc}`../library`. Without that interface, use the `NCSC` example as the starting point.

The convergence is logged in `DMFT/INFO_ITER`. Compare `Nd_latt` with `Nd_imp`, compare the lattice and impurity `(Sigoo - Vdc)` columns, and monitor the charge-difference column in the CSC run. Then perform post-processing from inside `DMFT`,

```bash
postDMFT.py ac --average 5
postDMFT.py dos
postDMFT.py bands --plot-plain --omega-points 1000 --band-k-points 1000 --normalize
```
