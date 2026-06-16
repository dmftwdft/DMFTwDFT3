# SrVO3 With SIESTA

Source directory: `examples/SrVO3_siesta`

This example uses SIESTA for SrVO3 with a V `d` plus O `p` Wannier subspace.

Included files:

- `input.toml`
- `para_com.dat`
- `DFT_mu.out`
- `SrVO3.fdf`
- `Sr.psf`
- `V.psf`
- `O.psf`

Files you must edit:

- `path_bin` in `input.toml`.
- `para_com.dat` for your MPI launcher.
- SIESTA executable setup in your environment or DMFTwDFT `bin` directory.

The SIESTA input already requests the Wannier90 files needed by DMFTwDFT:

```text
Siesta2Wannier90.WriteMmn       .true.
Siesta2Wannier90.WriteAmn       .true.
Siesta2Wannier90.WriteEig       .true.
Siesta2Wannier90.WriteUnk       .false.
Siesta2Wannier90.NumberOfBands 28
```

Key settings in `input.toml`:

- `Niter = 1`, so this is a non-charge-self-consistent DMFT run.
- `Nit = 2`, a short DMFT loop intended as an example starting point.
- `n_tot = 19`, for the SrVO3 V `d` and O `p` Wannier subspace.
- `cor_at = [["V1"]]`, with V `d` orbitals treated as correlated.
- `ewin = [-8, 6]`, relative to the DFT Fermi level.

Run from a copied and edited example directory:

```bash
DMFT.py -dft siesta -structurename SrVO3 -dmft
```

For the SIESTA Lowdin path, add `-lowdin`:

```bash
DMFT.py -dft siesta -structurename SrVO3 -lowdin -dmft
```

DMFTwDFT generates the Wannier90 input unless `-nowin` is supplied, runs Wannier90 preprocessing to produce `SrVO3.nnkp`, runs SIESTA, then runs Wannier90 and the DMFT loop.
