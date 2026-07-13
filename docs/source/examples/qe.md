# Quantum Espresso

The Quantum Espresso examples use QE and Wannier90 input/output files as the DFT input to DMFTwDFT. The examples include a standard QE workflow and a prepared QE/AiiDA reference workflow.

General QE setup requirements,

- Provide the Quantum Espresso pseudopotentials referenced by `pseudo_dir` and `ATOMIC_SPECIES`.
- Edit `pseudo_dir`, `outdir`, and other site-specific QE paths in the `.in` files.
- Set `path_bin` in `input.toml` to your local DMFTwDFT `bin` directory.
- Edit `para_com.dat` for your MPI launcher.
- Ensure QE executables and Wannier90 executables are available in your environment or DMFTwDFT `bin` directory.

Run a QE-backed DMFT calculation with,

```bash
DMFT.py dmft --dft qe --structure-name <seed> -v
```

For AiiDA-mode QE workflows, use,

```bash
DMFT.py dmft --dft qe --aiida -v
```

A list of QE examples is provided below.

```{toctree}
:maxdepth: 1

srvo3_qe
srvo3_qe_aiida
```
