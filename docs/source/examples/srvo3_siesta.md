# SrVO3

Source directory: `examples/SrVO3_siesta`

This example uses SIESTA for SrVO$_3$ with a V-$d$ $+$ O-$p$ Wannier subspace.

Included files,

- `input.toml`
- `para_com.dat`
- `SrVO3.fdf`
- `Sr.psf`
- `V.psf`
- `O.psf`

Material-specific files you must edit,

- `SrVO3.fdf` if you need to change SIESTA, structure, pseudopotential, or Wannier90 settings.

The SIESTA input already requests the Wannier90 files needed by DMFTwDFT,

```text
Siesta2Wannier90.WriteMmn       .true.
Siesta2Wannier90.WriteAmn       .true.
Siesta2Wannier90.WriteEig       .true.
Siesta2Wannier90.WriteUnk       .false.
Siesta2Wannier90.NumberOfBands 28
```

These flags tell SIESTA to write the matrix elements, projections, and eigenvalues used by Wannier90 and DMFTwDFT. `Siesta2Wannier90.NumberOfBands` should be large enough to include the localized orbitals that will be treated as correlated and hybridized states needed to describe the low-energy Wannier subspace. For SrVO$_3$, the example includes V-$d$ and O-$p$ states so that the V-$d$ correlated orbitals are represented inside a broader V-O Wannier manifold. This example uses 28 DFT bands and 14 Wannier bands for V-$d$ and O-$p$ states.

The `--structure-name SrVO3` option uses `SrVO3` as the SIESTA/Wannier seed. DMFTwDFT therefore expects files such as `SrVO3.fdf` and writes or reads seed-dependent Wannier files such as `SrVO3.nnkp`, `SrVO3.eig`, `SrVO3.amn`, `SrVO3.chk`, and `SrVO3.win` during the workflow.

Key settings in `input.toml`,

- `Niter = 1`, so this is a non-charge-self-consistent DMFT run.
- `Nit = 2`, a short DMFT loop intended as an example starting point.
- `n_tot = 19`, for the SrVO3 V-$d$ and O-$p$ Wannier subspace.
- `cor_at = [["V1"]]`, with V-$d$ orbitals treated as correlated.
- `ewin = [-8, 6]`, relative to the DFT Fermi level.

Run from a copied and edited example directory,

```bash
DMFT.py dmft --dft siesta --structure-name SrVO3 -v
```

DMFTwDFT generates the Wannier90 input unless `--no-win` is supplied, runs Wannier90 preprocessing to produce `SrVO3.nnkp`, runs SIESTA, then runs Wannier90 and the DMFT loop.

Once converged, run post-processing from inside `DMFT`,

```bash
postDMFT.py ac --average 5
postDMFT.py dos
postDMFT.py bands --plot-plain --omega-points 1000 --band-k-points 1000 --normalize
```
