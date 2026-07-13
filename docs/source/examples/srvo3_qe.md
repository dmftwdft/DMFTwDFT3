# SrVO3

Source directory: `examples/SrVO3_qe`

This example uses Quantum Espresso input files for SrVO$_3$ with a V-$d$ $+$ O-$p$ Wannier subspace.

Included files,

- `input.toml`
- `para_com.dat`
- `SrVO3.scf.in`
- `SrVO3.nscf.in`
- `SrVO3.pw2wannier90.in`

See {doc}`qe` for general Quantum Espresso setup requirements, including pseudopotentials, site-specific QE paths, `path_bin`, MPI launcher, and executable setup.

Key settings in `input.toml`,

- `Niter = 1`, so this is a non-charge-self-consistent DMFT run.
- `Nit = 5`, a short DMFT loop.
- `n_tot = 19`, for the SrVO$_3$ V-$d$ and O-$p$ Wannier subspace.
- `cor_at = [["V1"]]`, with V-$d$ orbitals treated as correlated.
- `ewin = [-8, 6]`, relative to the DFT Fermi level.

Run from a copied and edited example directory,

```bash
DMFT.py dmft --dft qe --structure-name SrVO3 -v
```

DMFTwDFT uses the `SrVO3` seed to identify QE and Wannier90 files such as `SrVO3.scf.in`, `SrVO3.nscf.in`, and `SrVO3.pw2wannier90.in`.

Once converged, run post-processing from inside `DMFT`,

```bash
postDMFT.py ac --average 5
postDMFT.py dos
postDMFT.py bands --plot-plain --omega-points 1000 --band-k-points 1000 --normalize
```
