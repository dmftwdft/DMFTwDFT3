# Utilities

The `utilities` directory contains optional helper scripts for plotting, analysis, batch checks, and specialized debugging. These are separate from the main workflow commands `DMFT.py` and `postDMFT.py`.

Most users should start with:

```bash
DMFT.py -h
postDMFT.py -h
```

Use the utilities when you need lower-level analysis or a quick diagnostic that is not covered by the main workflow.

## Running Utilities

The utilities are not a replacement for `DMFT.py` or `postDMFT.py`. They usually assume that DMFTwDFT has already been installed and that the `bin` directory is available through `PATH` and `PYTHONPATH`.

Run them by path from the expected working directory, for example:

```bash
python /path/to/DMFTwDFT3/utilities/plotDMFT.py -h
```

If you use them frequently, you can add the `utilities` directory to your shell `PATH` yourself. `setup.py` only adds the `bin` directory automatically.

## Plotting

| Utility | Run From | Purpose |
| --- | --- | --- |
| `plotDMFT.py` | A completed `DMFT` directory | Plots real and imaginary parts of `G_loc.out.*`, averaged `sig.inp.*`, and optionally `ac/Sig.out`. Writes PDFs under `plots`. |
| `plotDMFTDOS.py` | A directory containing `G_loc.out` from a DOS run | Produces a simple projected DOS plot `DMFT-PDOS.png`. This script has hard-coded orbital-column assumptions and may need editing for other orbital orderings. |

Example:

```bash
python /path/to/DMFTwDFT3/utilities/plotDMFT.py \
  -siglistindex 5 \
  -cor_orb_index 1 2 \
  -cor_orb_labels '$e_g$' '$t_{2g}$'
```

## Analysis

| Utility | Run From | Purpose |
| --- | --- | --- |
| `Z.py` | A completed `DMFT` directory | Estimates quasiparticle residue and effective mass from the low-frequency imaginary-axis self-energy files `sig.inp.*`. |
| `DMFT-total-energy.py` | A directory containing one `DMFT` run, or a batch root with numbered run directories | Reads `DMFT/INFO_ITER` and reports or tabulates averaged total-energy estimates. |
| `electron_count.py` | A DFT/DMFT setup directory with `input.toml` and DFT inputs | Estimates the total electron count in the Wannier manifold. This can help set `n_tot`. |

Examples:

```bash
python /path/to/DMFTwDFT3/utilities/Z.py -siglistindex 5 -cor_orb_index 1
python /path/to/DMFTwDFT3/utilities/DMFT-total-energy.py -navg 5
python /path/to/DMFTwDFT3/utilities/countDMFT.py -type dmft
```

## Batch Checks

| Utility | Run From | Purpose |
| --- | --- | --- |
| `countDMFT.py` | A batch root containing `DMFT` or `HF` directories, or numbered run directories | Checks whether DMFT/HF runs and selected post-processing steps are complete. Writes incomplete-run lists. |

Examples:

```bash
python /path/to/DMFTwDFT3/utilities/countDMFT.py -type dmft
python /path/to/DMFTwDFT3/utilities/countDMFT.py -type dmft -po ac dos
python /path/to/DMFTwDFT3/utilities/countDMFT.py -type dmft -p vacancy
```

## Specialized Or Legacy Helpers

These utilities are more specialized and may require material-specific files, interactive input, or edits before use.

| Utility | Run From | Purpose |
| --- | --- | --- |
| `hermitiancheck.py` | A directory containing `dmft-nkij.dat` or a specified equivalent file | Checks Hermiticity of a DMFT occupancy matrix dump and writes eigenvalue/diagonal summaries. |
| `oreo.py` | A VASP phonon/deformation analysis directory with `OUTCAR` | Extracts band shifts into `deltEps_*.deig` files. Interactive and specialized. |
| `Re_wt.py` | A VASP-derived deformation analysis directory with `OUTCAR` and `deltEps_*.deig` files | Reweights deformation data using mode components. Interactive and specialized. |
| `co_eff_phon.py` | A phonon analysis directory with `OUTCAR`, `DYNMAT`, and `deltEps_*.deig` files | Combines phonon-mode coefficients with deformation data. Interactive and specialized. |

Example:

```bash
python /path/to/DMFTwDFT3/utilities/hermitiancheck.py 28 512 dmft-nkij.dat
```

## Current Path

The directory was renamed from `scripts` to `utilities` to better describe its role. Current documentation uses `utilities`; older PDFs or notes may still refer to `/scripts`.
