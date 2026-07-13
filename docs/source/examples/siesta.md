# SIESTA

The SIESTA examples use the SIESTA/Wannier90 interface to generate the Wannier files needed by DMFTwDFT.

General SIESTA setup requirements:

- Include `input.toml`, `para_com.dat`, and optionally `para_com_dft.dat`.
- Provide the SIESTA input file `<seed>.fdf` and pseudopotential files such as `.psf`.
- Set `path_bin` in `input.toml` to your local DMFTwDFT `bin` directory.
- Ensure the SIESTA executable is available in your environment or DMFTwDFT `bin` directory.

The SIESTA `.fdf` file must request the Wannier90 files that DMFTwDFT needs:

```text
Siesta2Wannier90.WriteMmn .true.
Siesta2Wannier90.WriteAmn .true.
Siesta2Wannier90.WriteEig .true.
Siesta2Wannier90.WriteUnk .false.
Siesta2Wannier90.NumberOfBands 28
```

Adjust `Siesta2Wannier90.NumberOfBands` for the material and energy window. It should include the localized orbitals that will be treated as correlated and hybridized states needed to describe the low-energy Wannier subspace.

Run a SIESTA-backed DMFT calculation with,

```bash
DMFT.py dmft --dft siesta --structure-name <seed>
```

DMFTwDFT generates the Wannier90 input unless `--no-win` is supplied, runs Wannier90 preprocessing to create `<seed>.nnkp`, runs SIESTA, then runs Wannier90 and the DMFT loop.

The `--lowdin` flag is available for the SIESTA Lowdin workflow,

```bash
DMFT.py dmft --dft siesta --structure-name <seed> --lowdin
```

```{note}
Full charge-self-consistent SIESTA DMFT workflows are still under development.
```

A list of SIESTA examples is provided below.

```{toctree}
:maxdepth: 1

srvo3_siesta
```
