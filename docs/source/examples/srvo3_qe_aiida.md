# SrVO3 QE Through AiiDA

Source directory: `examples/SrVO3_qe_aiida`

This directory contains files from a QE/AiiDA workflow:

- `aiida.in`
- `aiida.out`
- `aiida.win`
- `aiida.wout`

The current directory is useful as prepared QE/AiiDA reference material, but it is not a complete launch directory for `DMFT.py dmft --aiida` as committed.

For a current AiiDA-mode DMFTwDFT run, `DMFT.py` expects files including:

- `input.toml`
- `para_com.dat`
- `aiida.win`
- `aiida.eig`
- `aiida.chk`
- `aiida.amn`

The `DMFT.py dmft --aiida` path copies the AiiDA/Wannier files to the standard DMFTwDFT names:

```text
aiida.eig -> wannier90.eig
aiida.chk -> wannier90.chk
aiida.win -> wannier90.win
aiida.amn -> wannier90.amn
```

After adding the missing files and configuring `input.toml`, run from the calculation directory:

```bash
DMFT.py dmft --dft qe --aiida --verbose
```

If you use a structure name with the AiiDA workflow, keep it consistent with the seed names in the generated QE/Wannier files.
