# LaNiO3 With VASP

Source directories:

- `examples/LaNiO3_vasp/NCSC`
- `examples/LaNiO3_vasp/CSC`

These examples reproduce the LaNiO3 material used throughout the historical PDF tutorials. The non-charge-self-consistent and charge-self-consistent examples use the same Ni `d` plus O `p` Wannier subspace but different loop settings.

Included files in each subdirectory:

- `input.toml`
- `INCAR`
- `KPOINTS`
- `POSCAR`
- `submit.sh`

Files you must provide or edit:

- `POTCAR`, because VASP pseudopotentials are not distributed with the repository.
- `path_bin` in `input.toml`.
- `para_com.dat`, or an updated submission script that writes it.
- VASP executable setup in your environment or DMFTwDFT `bin` directory.

The bundled `submit.sh` files are historical cluster scripts. They contain site-specific modules and call `RUNDMFT.py` directly. For current usage, prefer `DMFT.py` unless you are intentionally debugging the lower-level runner.

The non-charge-self-consistent example has:

- `Niter = 1`
- `Nit = 15`
- `n_tot = 50.0`
- `nf = 7.0`
- `L_rot = [1, 0]`, rotating the Ni local axes.
- `cor_at = [["Ni1", "Ni2"]]`
- `ewin = [-8, 3.1]`

Run from a copied and edited `NCSC` directory:

```bash
DMFT.py dmft --dft vasp
```

The charge-self-consistent example has:

- `Niter = 30`
- `Ndft = 10`
- `Nit = 1`
- The same Ni/O correlated subspace settings as the NCSC case.

Run from a copied and edited `CSC` directory:

```bash
DMFT.py dmft --dft vasp
```

Charge-self-consistent VASP workflows require the VASP-side DMFTwDFT interface described in {doc}`../installation` and {doc}`../library`. Without that interface, use the `NCSC` example as the starting point.

The key convergence file is `DMFT/INFO_ITER`. For LaNiO3, compare `Nd_latt` with `Nd_imp`, compare the lattice and impurity `(Sigoo - Vdc)` columns, and monitor the charge-difference column in the CSC run.
