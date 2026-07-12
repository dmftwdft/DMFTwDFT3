# Utilities

The `utilities` directory contains optional helper scripts for plotting, analysis, batch checks, and specialized debugging. These are separate from the main workflow commands `DMFT.py` and `postDMFT.py`.

Most users should start with:

```bash
DMFT.py -h
postDMFT.py -h
```

Use the utilities when you need lower-level analysis or a quick diagnostic that is not covered by the main workflow.

## Running Utilities

The utilities are not a replacement for `DMFT.py` or `postDMFT.py`. After running `setup.py` and restarting or sourcing your shell startup file, the `utilities` directory should already be available through `PATH`, and the `bin` directory should be available through both `PATH` and `PYTHONPATH`.

You can then run utilities by name from the expected working directory, for example:

```bash
plotDMFT.py -h
```

If your shell has not been refreshed or you have not installed the path settings, run utilities by full path:

```bash
python /path/to/DMFTwDFT3/utilities/plotDMFT.py -h
```

If the command name is not found after setup, restart the shell or source the startup file printed by `setup.py`.

## Plotting and Analysis

`plotDMFT.py`
: Run from a completed `DMFT` directory. Plots real and imaginary parts of `G_loc.out.*`, averaged `sig.inp.*`, and optionally `ac/Sig.out`. Writes PDFs under `plots`.

```bash
python /path/to/DMFTwDFT3/utilities/plotDMFT.py \
  --average 5 \
  --cor-orb-index 1 2 \
  --cor-orb-labels '$e_g$' '$t_{2g}$'
```

`plotDMFTDOS.py`
: Run from a directory containing `G_loc.out` from a DOS run. Produces a simple projected DOS plot, `DMFT-PDOS.png`. This script has hard-coded orbital-column assumptions and may need editing for other orbital orderings.

```bash
python /path/to/DMFTwDFT3/utilities/plotDMFTDOS.py
```

`Z.py`
: Run from a completed `DMFT` directory. Estimates quasiparticle residue and effective mass from the low-frequency imaginary-axis self-energy files `sig.inp.*`.

```bash
python /path/to/DMFTwDFT3/utilities/Z.py --average 5 --cor-orb-index 1
```

`DMFT_total_energy.py`
: Run from a directory containing one `DMFT` run, or from a batch root with numbered run directories. Reads `DMFT/INFO_ITER` and reports or tabulates averaged total-energy estimates.

```bash
python /path/to/DMFTwDFT3/utilities/DMFT_total_energy.py --average 5
```

## Batch Checks and Diagnostics

`electron_count.py`
: Run from a DFT/DMFT setup directory with `input.toml` and DFT inputs. Estimates the total electron count in the Wannier manifold. This can help set `n_tot`.

```bash
python /path/to/DMFTwDFT3/utilities/electron_count.py --dft siesta --structure-name SrVO3
```

`countDMFT.py`
: Run from a batch root containing `DMFT` or `HF` directories, or numbered run directories. Checks whether DMFT/HF runs and selected post-processing steps are complete. Writes incomplete-run lists.

```bash
python /path/to/DMFTwDFT3/utilities/countDMFT.py --type dmft
python /path/to/DMFTwDFT3/utilities/countDMFT.py --type dmft --post ac dos
python /path/to/DMFTwDFT3/utilities/countDMFT.py --type dmft --pattern vacancy
```

`hermitiancheck.py`
: Run from a directory containing `dmft-nkij.dat` or a specified equivalent file. Checks Hermiticity of a DMFT occupancy matrix dump and writes eigenvalue/diagonal summaries.

```bash
python /path/to/DMFTwDFT3/utilities/hermitiancheck.py 28 512 dmft-nkij.dat
```

## Current Path

The directory was renamed from `scripts` to `utilities` to better describe its role. Current documentation uses `utilities`; older PDFs or notes may still refer to `/scripts`.
