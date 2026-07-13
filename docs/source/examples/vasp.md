# VASP

The VASP examples use VASP-generated Wannier90 files as the DFT input to DMFTwDFT. VASP pseudopotentials are not distributed with DMFTwDFT, so provide the required `POTCAR` files before running these examples.

General VASP setup requirements,

- Provide `POTCAR` in each copied run directory.
- Set `path_bin` in `input.toml` to your local DMFTwDFT `bin` directory.
- Edit `para_com.dat` for your MPI launcher.
- Ensure the VASP executable is available in your environment or DMFTwDFT `bin` directory.
- Use the same MPI stack for Python, DMFTwDFT executables, impurity solvers, Wannier90, and VASP.

Run a VASP-backed DMFT calculation with,

```bash
DMFT.py dmft --dft vasp -v
```

Charge-self-consistent VASP workflows require the VASP-side DMFTwDFT interface described in {doc}`../installation` and {doc}`../library`. Without that interface, use the non-charge-self-consistent examples as starting points.

Examples are listed below.

```{toctree}
:maxdepth: 1

srvo3_vasp
lanio3_vasp
```
