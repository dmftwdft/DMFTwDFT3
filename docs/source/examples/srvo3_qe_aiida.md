# SrVO3 through AiiDA

Source directory: `examples/SrVO3_qe_aiida`

This directory contains files from a QE/AiiDA workflow,

- `aiida.in`
- `aiida.out`
- `aiida.win`
- `aiida.wout`

These are generated through an AiiDA workflow that runs QE and Wannier90, and produces the files needed by DMFTwDFT.
For a complete AiiDA-mode DMFTwDFT run, `DMFT.py` expects files including,

- `input.toml`
- `para_com.dat`
- `aiida.out`
- `aiida.win`
- `aiida.eig`
- `aiida.chk`
- `aiida.amn`

After generating the required files and configuring `input.toml`, run from the calculation directory,

```bash
DMFT.py dmft --dft qe --aiida -v
```

Once converged, run post-processing from inside `DMFT`,

```bash
postDMFT.py ac --average 5
postDMFT.py dos
postDMFT.py bands --plot-plain --omega-points 1000 --band-k-points 1000 --normalize
```
