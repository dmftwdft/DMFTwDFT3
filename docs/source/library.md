(labellibrary)=
# Library Mode

DMFTwDFT includes a library mode that can be linked into DFT codes to enable full charge-self-consistent DFT+DMFT calculations. The library exposes Fortran routines that return the DMFT occupancy information needed to update the charge density inside an external DFT code.

Specifically, the DFT code passes its k-point list and weights to `Compute_DMFT()` and receives:

- `band_win_loc`: the Wannier-subspace band range at each k-point
- `DMFT_eval`: eigenvalues of the DMFT occupancy matrix
- `DMFT_evec`: eigenvectors of the DMFT occupancy matrix

The implementation is in `sources/src/dmft_lib.F90`. A small example is provided in `examples/library_mode_test`. Compilation details are summarized in {doc}`installation`.

## Charge Density Formalism

The total charge density is split into states outside the Wannier window and the DMFT contribution inside the window:

```{math}
\rho(r) = \sum_{i \notin W} \rho_i^{DFT}(r) + \sum_{i,j \in W} \rho_{ij}^{DMFT}(r)
```

where `W` is the energy window used to construct the Wannier subspace.

Within the Wannier window, the DMFT charge density can be represented using DFT Kohn-Sham wavefunctions:

```{math}
\rho_{ij}^{DMFT}(r) = \frac{1}{N_k} \sum_k n_{kij}
\langle \psi^{KS}_{ki} | r \rangle
\langle r | \psi^{KS}_{kj} \rangle
```

Here `n_{kij}` is the DMFT occupancy matrix in the Kohn-Sham basis. Because this matrix is Hermitian, it can be diagonalized at each k-point:

```{math}
n_{kij} = \sum_\lambda U^{DMFT}_{ki\lambda} w_{k\lambda} U^{DMFT*}_{kj\lambda}
```

The DFT code can then form DMFT-weighted wavefunctions from the returned eigenvectors and use the eigenvalues as occupations:

```{math}
\langle r | \psi^{DMFT}_{k\lambda} \rangle = \sum_i
\langle r | \psi^{KS}_{ki} \rangle U^{DMFT}_{ki\lambda}
```

```{math}
\rho^{DMFT}(r) = \frac{1}{N_k} \sum_{k,\lambda} w_{k\lambda}
\langle \psi^{DMFT}_{k\lambda} | r \rangle
\langle r | \psi^{DMFT}_{k\lambda} \rangle
```

This is the same high-level approach described in the historical PDF manuals, but the current source location and routine names are listed below.

## Fortran Interface

The main library entry point is:

```fortran
subroutine Compute_DMFT(n_kpts_loc, n_wann, kpt_dft, wght_dft, &
                        band_win_loc, DMFT_eval, DMFT_evec)
```

Inputs:

`n_kpts_loc`
: Number of DFT k-points passed by the host DFT code. These can be irreducible-zone or full-zone k-points, depending on the host implementation.

`n_wann`
: Number of Wannier orbitals, equal to the size of the Wannier Hamiltonian.

`kpt_dft(3, n_kpts_loc)`
: DFT k-points in fractional coordinates.

`wght_dft(n_kpts_loc)`
: DFT k-point weights. The weights should sum to one.

Outputs:

`band_win_loc(2, n_kpts_loc)`
: Band range of the Wannier subspace at each k-point.

`DMFT_eval(n_wann, n_kpts_loc)`
: Eigenvalues `w_{k lambda}` of the DMFT occupancy matrix.

`DMFT_evec(n_wann, n_wann, n_kpts_loc)`
: Eigenvectors `U^{DMFT}_{ki lambda}` of the DMFT occupancy matrix.

There is also a related entry point:

```fortran
subroutine Compute_DMFT_from_amn(n_kpts_loc, n_wann, kpt_dft, wght_dft, &
                                 band_win_loc, DMFT_eval, DMFT_evec)
```

This variant additionally reads Wannier90 `amn` information and computes the unitary transformation from it.

## Required Runtime Files

The library routine reads the same DMFT/Wannier state used by the standalone executables, including files such as:

- `seedname.dat`
- `wannier90.chk`
- `wannier90.eig`
- `sig.inp`
- `dmft_params.dat`

The exact set depends on which library entry point is used. Generate the Wannier checkpoint first; the bundled `examples/library_mode_test/README.txt` currently notes this requirement explicitly.

## External DFT Integration

An external DFT code is responsible for:

- Passing its k-points and normalized weights into the library.
- Removing or replacing the ordinary DFT contribution from bands inside the correlated Wannier window.
- Building the DMFT charge-density contribution using `DMFT_eval`, `DMFT_evec`, and the host code's Kohn-Sham wavefunctions or basis representation.
- Feeding the updated charge density into the next DFT step.

For a detailed explanation of DMFTwDFT, refer to the documents in the `manuals` directory and the articles [DMFTwDFT](https://arxiv.org/abs/2002.00068) and [PhysRevB.90.235103](https://journals.aps.org/prb/pdf/10.1103/PhysRevB.90.235103).
