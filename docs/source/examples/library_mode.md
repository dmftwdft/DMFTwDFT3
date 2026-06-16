# Library Mode Test

Source directory: `examples/library_mode_test`

This example demonstrates calling the DMFT library interface from Fortran. It is intended for developers integrating DMFTwDFT into a DFT code for charge self-consistency.

Included files include:

- `test.F90`
- `Makefile`
- `make.inc`
- `dmft_params.dat`
- `sig.inp`
- `wannier90.eig`
- `DMFT_mu.out`
- `INFO_DFT_loop`
- historical run outputs and submission files

The example program builds an 8 x 8 x 8 uniform k-mesh, assigns normalized k-point weights, calls `Compute_DMFT`, and prints representative `band_win`, `DMFT_eval`, and `DMFT_evec` values.

The core call in `test.F90` is:

```fortran
call Compute_DMFT(nkpts, num_wann, kpts, wght, band_win, DMFT_eval, DMFT_evec)
```

Before compiling:

- Build DMFTwDFT so `libdmft.a` is available.
- Generate or provide the matching `wannier90.chk` file. The example README notes this requirement.
- Ensure `make.inc` points to the same compiler, MPI, and library stack used to build DMFTwDFT.
- Make `libdmft.a` visible to the link line, for example by copying it into the example directory or editing `LIBS`/library paths.

Compile and run from a copied and edited example directory:

```bash
make
mpirun -np 4 ./test.x
```

The historical `submit.sh` is site-specific and should be treated as a template only.

For the full library interface description and charge-density equations, see {doc}`../library`.
