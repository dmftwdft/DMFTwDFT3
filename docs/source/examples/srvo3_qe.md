# SrVO3 With Quantum Espresso

Source directory: `examples/SrVO3_qe`

This example uses Quantum Espresso input files for SrVO3 with a V `d` plus O `p` Wannier subspace.

Included files:

- `input.toml`
- `para_com.dat`
- `SrVO3.scf.in`
- `SrVO3.nscf.in`
- `SrVO3.pw2wannier90.in`

Files you must provide or edit:

- Quantum Espresso pseudopotentials referenced by `pseudo_dir` and `ATOMIC_SPECIES`.
- `pseudo_dir`, `outdir`, and other site-specific QE paths in the `.in` files.
- `path_bin` in `input.toml`.
- `para_com.dat` for your MPI launcher.
- QE executables and Wannier90 executables in your environment or DMFTwDFT `bin` directory.

Key settings in `input.toml`:

- `Niter = 1`, so this is a non-charge-self-consistent DMFT run.
- `Nit = 30`, a longer DMFT loop than the short VASP/SIESTA SrVO3 examples.
- `n_tot = 19`, for the SrVO3 V `d` and O `p` Wannier subspace.
- `cor_at = [["V1"]]`, with V `d` orbitals treated as correlated.
- `ewin = [-8, 6]`, relative to the DFT Fermi level.
- Optional `num_bands_win` and `exclude_bands` are present as commented examples.

Run from a copied and edited example directory:

```bash
DMFT.py dmft --dft qe --structure-name SrVO3
```

DMFTwDFT uses the `SrVO3` seed to identify QE and Wannier90 files such as `SrVO3.scf.in`, `SrVO3.nscf.in`, and `SrVO3.pw2wannier90.in`.
