(labellibrary)=

# Library Mode

DMFTwDFT includes a library mode that can be linked into DFT codes to enable full charge-self-consistent DFT+DMFT calculations. The library exposes Fortran routines that return the DMFT occupancy information needed to update the charge density inside an external DFT code.

Specifically, the DFT code passes its k-point list and weights to `Compute_DMFT()` and receives,

- `band_win_loc`: the Wannier-subspace band range at each k-point
- `DMFT_eval`: eigenvalues of the DMFT occupancy matrix
- `DMFT_evec`: eigenvectors of the DMFT occupancy matrix

The implementation is in `sources/src/dmft_lib.F90`. A small example is provided in `examples/library_mode_test`. Compilation details are summarized in {doc}`installation`.

## Charge Density Formalism

The total charge density is split into states outside the Wannier window and the DMFT contribution inside the window,

```{math}
\rho(r) = \sum_{i \notin W} \rho_i^{DFT}(r) + \sum_{i,j \in W} \rho_{ij}^{DMFT}(r)
```

where $W$ is the energy window used to construct the Wannier subspace, $\rho_{ij}^{DMFT}(r)$ is the charge density within the DMFT subspace, and $i$, $j$ are the band indices.

Within the Wannier window, the DMFT charge density can be represented using DFT Kohn-Sham wavefunctions at momentum $k$ and band $j$, $|\psi^{KS}_{kj} \rangle$,

```{math}
\rho_{ij}^{DMFT}(r) = \frac{1}{N_k} \sum_k n_{kij}
\langle \psi^{KS}_{ki} | r \rangle
\langle r | \psi^{KS}_{kj} \rangle
```

Here, $n_{kij}$ is the DMFT occupancy matrix in the Kohn-Sham basis. Because this matrix is Hermitian, it can be diagonalized at each $k$-point,

```{math}
n_{\vec{k} i j}=\sum_{\lambda} U_{\vec{k} i \lambda}^{DMFT} \cdot w_{\vec{k} \lambda} \cdot U_{\vec{k} j \lambda}^{DMFT*}
```

terms of eigenvalues $w_{\vec{k} \lambda}$ and eigenfunctions $\phi_{\lambda}$.
$U^{DMFT}_{ki\lambda}$ are unitary matrices whose rows are $\phi_{\lambda}$s. Using this eigen-decomposition, the wavefunction $\psi^{KS}$ is unitarily transformed to $\psi^{DMFT}_{k\lambda}$ given by,

```{math}
\langle r | \psi^{DMFT}_{k\lambda} \rangle = \sum_i
\langle r | \psi^{KS}_{ki} \rangle U^{DMFT}_{ki\lambda}
```

The charge density $\rho^{DMFT}(r)$ can be represented using the DMFT weights and DMFT wavefunctions using the subroutine to compute the charge density within any DFT code.

```{math}
\rho^{DMFT}(r) = \frac{1}{N_k} \sum_{k,\lambda} w_{k\lambda}
\langle \psi^{DMFT}_{k\lambda} | r \rangle
\langle r | \psi^{DMFT}_{k\lambda} \rangle
```

Practically, a host DFT code should keep the ordinary DFT contribution from states outside the Wannier window and replace the DFT occupations inside the Wannier window with the DMFT occupancy matrix. The updated density is then used in the next DFT step, and the process is repeated until both the DFT charge density and DMFT self-energy are stable.

## Fortran Interface

The main library entry point is,

```fortran
subroutine Compute_DMFT(n_kpts_loc, n_wann, kpt_dft, wght_dft, band_win_loc, DMFT_eval, DMFT_evec)
```

**Inputs**

1. `n_kpts_loc` : Number of DFT k-points passed by the host DFT code. These can be irreducible-zone or full-zone k-points, depending on the host implementation.

2. `n_wann` : Number of Wannier orbitals, equal to the size of the Wannier Hamiltonian.

3. `kpt_dft(3, n_kpts_loc)` : DFT k-points in fractional coordinates.

4. `wght_dft(n_kpts_loc)` : DFT k-point weights. The weights should sum to one.

**Outputs**

1. `band_win_loc(2, n_kpts_loc)` : Band range of the Wannier subspace at each k-point.

2. `DMFT_eval(n_wann, n_kpts_loc)` : Eigenvalues $w_{k \lambda}$ of the DMFT occupancy matrix.

3. `DMFT_evec(n_wann, n_wann, n_kpts_loc)` : Eigenvectors of the DMFT occupancy matrix.

There is also an alternate entry point,

```fortran
subroutine Compute_DMFT_from_amn(n_kpts_loc, n_wann, kpt_dft, wght_dft, band_win_loc, DMFT_eval, DMFT_evec)
```

This variant additionally reads Wannier90 `amn` information and computes the unitary transformation from it.

## External DFT Integration

An external DFT code is responsible for,

- Passing its k-points and normalized weights into the library.
- Removing or replacing the ordinary DFT contribution from bands inside the correlated Wannier window.
- Building the DMFT charge-density contribution using `DMFT_eval`, `DMFT_evec`, and the host code's Kohn-Sham wavefunctions or basis representation.
- Feeding the updated charge density into the next DFT step.

Please refer to [Park _et al._, Phys. Rev. B **90**, 235103 (2014)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.90.235103) and [Singh, V., Herath, U., _et al._ Comput. Phys. Commun. **261**, 107778 (2021)](https://doi.org/10.1016/j.cpc.2020.107778) for a detailed discussion of the charge density formalism.
