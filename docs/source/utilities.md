# Utilities

The `utilities` directory contains helper scripts for plotting, analysis, and debugging tasks. These are separate from the main workflow commands `DMFT.py` and `postDMFT.py`.

After running `setup.py` and restarting or sourcing your shell startup file, the `utilities` directory should already be available through `PATH`, and the `bin` directory should be available through both `PATH` and `PYTHONPATH`.

You can then run utilities by name from the expected working directory, for example,

```bash
plotDMFT.py -h
```

If your shell has not been refreshed or you have not installed the path settings, run utilities by full path:

```bash
python /path/to/DMFTwDFT3/utilities/plotDMFT.py -h
```

## Plotting and Analysis

### 1. `plotDMFT.py`

Plots real and imaginary parts of the Green's function `G_loc.out.*`, averaged self-energy `sig.inp.*`, and optionally analytically continued self-energy (if available) `ac/Sig.out`. Generates figures under `plots`.
Run from a completed `DMFT` directory. The Green's function is taken from the last `G_loc.out.*` iteration file without averaging; `--average` applies only to `sig.inp.*`.

The order of the columns are,

```text
|---------------------| |-----------------------|----------------------------|
| Matsubara Frequency | | Real part of SE       | Imaginary part SE          | x Repeats for each group
|---------------------| |-----------------------|----------------------------|   of "cor_orb".
```

This layout applies to the imaginary-axis files `G_loc.out.*` and `sig.inp.*`. `ac/Sig.out` uses the same one-pair-per-`cor_orb`-group ordering, but its first column is the real frequency $\omega$ rather than a Matsubara frequency. See {ref}`post-processing-data-files` for the post-processing file formats.

Note that `--cor-orb-index` indexes `cor_orb` groups, not Wannier orbitals. It is unrelated to the `--wannier-orbitals` indexing used by `postDMFT.py bands`, which is described in {ref}`wannier-orbital-order`.

Usage,

```text
plotDMFT.py
    --average <# of self energy files to average>
    --cor-orb-index <List of cor_orb indexes>
    --cor-orb-labels <Names of cor_orb's>
```

E.g., for correlated d-orbitals considering eg and t2g i.e.

```
"cor_orb": [[['d_z2','d_x2y2'],['d_xz','d_yz','d_xy']]]
```

run,

```shell
plotDMFT.py --average 5 --cor-orb-index 1 2 --cor-orb-labels '$e_g$' '$t_{2g}$'
```

### 2. `plotDMFTDOS.py`

Produces a simple projected DOS plot, `DMFT-PDOS.png`. This script has hard-coded orbital-column assumptions and may need editing for other orbital orderings. Intended for manual investigation of DOS results, when `postDMFT.py dos` is not sufficient.
Run from a directory containing `G_loc.out` from a DOS run, that is `dos/G_loc.out`.

```{warning}
Two different files are named `G_loc.out`. The one in the `DMFT` directory is on the imaginary axis with one column pair per `cor_orb` group, while `dos/G_loc.out` is on the real axis with one column pair per Wannier orbital. This script and {ref}`post-processing-data-files` refer to the latter.

The hard-coded columns are 2 and 8, the imaginary parts of Wannier orbitals 1 and 4, which are the $e_g$ pair for a single correlated $d$ atom. For any other orbital grouping, edit the script or use `postDMFT.py dos`. See {ref}`wannier-orbital-order`.
```

```bash
plotDMFTDOS.py
```

### 3. `Z.py`

Estimates quasi-particle residue (Z) and effective mass (m*/m) from the imaginary-axis self-energy files `sig.inp.*`. Averages a given number of self-energy files.
Run from a completed `DMFT` directory.

The order of the columns in sig.inp are,

```text
|---------------------| |-----------------------|----------------------------|
| Matsubara Frequency | | Real part of SE       | Imaginary part SE          | x Repeats for each group
|---------------------| |-----------------------|----------------------------|   of "cor_orb".
```

The data rows are preceded by header lines giving `nom`, `ncor_orb`, the temperature, `s_oo-Vdc`, `s_oo`, and `Vdc`.

Usage,

```text
Z.py --average <# of self energy files to average>
     --cor-orb-index <index of cor_orb>
```

For example,

```bash
Z.py --average 5 --cor-orb-index 1
```

### 4. `DMFT_total_energy.py`

Reads `DMFT/INFO_ITER` and reports or tabulates averaged total-energy estimates. Run from a directory containing one `DMFT` run, or from a batch root with numbered run directories.

```bash
DMFT_total_energy.py --average 5
```

## Diagnostics

### 1. `electron_count.py`

Estimates the total electron count in the Wannier manifold. This can help set `n_tot` in `input.toml`.
Run from a directory with `input.toml` and DFT inputs. It takes the `atomnames`, `orbs`, `cor_at` and `cor_orb` from `input.toml`.

E.g., for a SrVO$_3$ SIESTA setup, run,

```bash
electron_count.py --dft siesta --structure-name SrVO3
```

### 2. `countDMFT.py`

Checks whether DMFT/HF runs and selected post-processing steps are complete. Writes incomplete-run lists. Run from a batch root containing `DMFT` or `HF` directories, or numbered run directories. Use the flag `--pattern` to match folder name prefixes containing DMFT calculations.

```bash
countDMFT.py --type dmft
countDMFT.py --type dmft --post ac dos
countDMFT.py --type dmft --pattern vacancy
```

### 3. `hermitiancheck.py`

Checks Hermiticity of a DMFT occupancy matrix ($n_{kij}$) and writes eigenvalue/diagonal summaries. Run from a directory containing `dmft-nkij.dat`. This is generated when performing full charge self-consistent DMFT runs or through the DMFT library mode.

The shape of $n_{kij}$ : [iband, jband, kpoints]

The way $n_{kij}$ is saved in dmft-nkij.dat is with jband being the fastest index, iband being the next fastest and kpoints being the slowest index.

Usage,

```shell
hermitiancheck.py numberofbands numberofkpoints <optional: filename>
```

E.g., for a SrVO$_3$ DMFT run with 28 bands and 512 k-points, run,

```bash
hermitiancheck.py 28 512 dmft-nkij.dat
```
