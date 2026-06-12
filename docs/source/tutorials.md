# Tutorials

The following tutorials explain the usage of DMFTwDFT. Example files required to run these calculations are available in the `/examples` directory in the GitHub repository.

To perform a DFT+DMFT calculation, the following files should be present within the calculation directory:

- `INPUT.py`: contains the input parameters that govern the DMFT calculation.
- `para_com.dat`: contains the number of processors used for the DMFT calculation, such as `mpirun -np 32`.
- DFT files: input files required to launch an initial DFT calculation to initialize the DMFT calculation. AiiDA files are from a completed DFT calculation.
- VASP: `POSCAR`, `KPOINTS`, `POTCAR`, `INCAR`
- Siesta: `.fdf`, `.psf`
- QE: `.scf.in`, `.nscf.in`, `.pw2wannier90.in`
- QE through AiiDA: `aiida.amn`, `aiida.chk`, `aiida.eig`, `aiida.mmn`, `aiida.out`, `aiida.win`

Before you start, add the `bin` directory path in `INPUT.py` as the value for the key `path_bin`.

For example:

```python
"path_bin": "~/Dropbox/git/DMFTwDFT/bin/"
```

## DFT+DMFT Calculation

DFT+DMFT calculations are performed through the `DMFT.py` script. Since the DMFTwDFT `bin` directory is in the `PATH` variable, `DMFT.py` can be run from any calculation directory.

To get a description of its options, run:

```bash
DMFT.py -h
```

This script has the following options:

`dft`
: The choice of DFT code. Currently, `vasp`, `siesta`, and `qe` (Quantum Espresso) are supported. Quantum Espresso is supported through AiiDA, so for this case use the `-aiida` flag as well.

`relax`
: This flag turns on DFT convergence testing. If the forces are not converged, a convergence calculation is attempted. If it fails, the user is asked to modify convergence parameters. This is useful for vacancy and defect calculations where force convergence is required after the vacancy or defect is created in order to obtain a relaxed structure to perform DFT+DMFT with. Currently supported for VASP. This uses PyChemia to check for convergence. The relaxation occurs inside a `DFT_relax` directory.

`structurename`
: DFT codes such as Siesta use input files that contain the name of the system, for example $SrVO_3.fdf$. Therefore, when performing DFT+DMFT calculations with Siesta, this flag is required.

`dmft`
: This flag performs the DMFT calculation using the results from the DFT calculation if a previous DMFT calculation in the same directory is incomplete.

`hf`
: This flag performs the Hartree-Fock (HF) calculation to the correlated orbitals specified in `INPUT.py` if a previous HF calculation in the same directory is incomplete.

`force`
: This flag forces a DMFT or HF calculation even if a previous calculation has been completed. The option to check for completeness is helpful when running many DMFT/HF jobs on a cluster.

`kmeshtol`
: This controls the tolerance of two k-points belonging to the same shell in the Wannier90 calculation.

`aiida`
: Flag for AiiDA calculations. Currently, Quantum Espresso is supported through AiiDA.

`v`
: Flag to enable verbosity.

The calculations are performed in an automatically generated `DMFT` or `HF` directory where the script was run from.

Examples:

```bash
DMFT.py -dft vasp -relax -dmft
DMFT.py -dft siesta -structurename SrVO3 -dmft
DMFT.py -dft qe -structurename SrVO3 -dmft
DMFT.py -dft qe -aiida -dmft -v
```

## DMFT Post-Processing

DMFT post-processing is performed with the `postDMFT.py` script.

To get a description of the options, run:

```bash
postDMFT.py -h
```

This script performs analytical continuation, density of states, and band structure calculations on the DMFT/HF data. Once the DMFT/HF calculations are complete, this script should be initiated within the `DMFT` or `HF` directories.

This script has the following options:

`ac`
: Performs Analytic Continuation to obtain the Self Energies on the real axis. It has the option `-siglistindx` to specify the last number of Self Energy files (`sig.inp`) to average for the calculation.

`dos`
: Performs the partial density of states of the correlated orbitals. It has the following options:

- `-emin`: minimum energy value for interpolation
- `-emax`: maximum energy value for interpolation
- `-rom`: number of Matsubara frequency ($\omega$) points
- `-broaden`: broadening of the DOS
- `-show`: display the density of states
- `-elim`: energy range to plot

`bands`
: Performs the DMFT band structure calculations. It has the following options:

- `-emin`: minimum energy value for interpolation
- `-emax`: maximum energy value for interpolation
- `-rom`: number of Matsubara frequency ($\omega$) points
- `-kpband`: number of k-points for band structure calculation
- `-kn`: list of labels for k-points
- `-kp`: list of k-points corresponding to the k-point labels
- `-plotplain`: flag to plot a plain band structure
- `-plotpartial`: flag to plot a projected band structure
- `-sp`: flag to plot spin-polarized band structure
- `-wo`: list of Wannier orbitals to project onto the band structure
- `-vlim`: spectral intensity range
- `-show`: display the bands

The projected bands are especially helpful in determining the contribution to bands from different orbitals. The ordering is equivalent to the Wannier90 orbital order.

The calculations are stored in the `ac`, `dos`, and `bands` directories, respectively.

Examples:

```bash
postDMFT.py ac -siglistindx 4
postDMFT.py dos -show
postDMFT.py bands -plotplain
postDMFT.py bands -plotpartial -wo 4 5 6
postDMFT.py bands -sp -show
```
