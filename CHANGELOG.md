# Changelog

## 2.5.1 - 2026-08-07

- Fixed the uniform k-mesh allocation in `generate_kpts.F90` to use `num_new_kpts=qx*qy*(qz/2+1)` instead of `qx*qx*(qz/2+1)`. The previous expression under-allocated the k-point and weight arrays whenever `q_y > q_x`, so the k-point loop wrote past the end of both. This affected every non-charge-self-consistent DMFT k-sum and every density of states calculation, since `dmft.x` and `dmft_dos.x` both call `generate_uniform_kmesh`. Meshes with `q_x = q_y` were unaffected. The same correction was applied to the legacy `dmft_ksum.f`, `dmft_ksum_dos.f`, and `dmft_ksum_sp.f`, which are built but no longer installed or invoked.
- Removed `sources/dmft_ksum/fort_kpt_tools.f`, a duplicate of `sources/fort_kpt_tools/fort_kpt_tools.f` that no build rule referenced. The copy under `sources/fort_kpt_tools` is the one compiled into `fort_kpt_tools.so` and imported by `XHF0.py`.

## 2.5.0 - 2026-08-07

- Added `kmesh_tol_win`, `num_iter_win`, `dis_num_iter_win` keywords as input arguments in `input.toml` to control the Wannier90 k-mesh tolerance and number of iterations for disentanglement.

## 2.4 - 2026-07-31

- Removed the `path_bin` setting from `input.toml`. The `bin` directory is now derived from the installed package location, so no path configuration is required. Existing `input.toml` files that still set `path_bin` continue to load; the value is ignored.
- Added `bin_paths.py`, which resolves DMFTwDFT executables, scripts, and data files against the installed `bin` directory.
- Resolved external executables (`wannier90.x`, `w90chk2chk.x`, `vasp_std`, `siesta`, `pw.x`, `pw2wannier90.x`) from `bin`, falling back to `PATH` when not present there.
- Replaced the separate `vaspDMFT` executable with `vasp_std` for charge self-consistent calculations. A VASP built with the DMFT modifications runs both one-shot and charge self-consistent calculations, so only one executable is needed. Existing charge self-consistent setups must rename `bin/vaspDMFT` to `bin/vasp_std`.
- Replaced the hardcoded `pw2wannier90.x` invocation with a configurable executable attribute.
- Fixed `~` and trailing-slash handling for `bin` paths, which previously depended on the exact `path_bin` string.
- Documented cloning the repository and supplying Wannier90 and DFT executables as installation steps.

## 2.3 - 2026-07-11

- Changed `DMFT.py` and `postDMFT.py` input argument formats to use standard subcommands, short options, and long `--option-name` arguments.

## 2.2 - 2026-06-15

- Added automatic shell setup in `setup.py` for `PATH` and `PYTHONPATH`.
- Updated macOS setup guidance for Apple Silicon and Homebrew OpenMPI.
- Improved subprocess handling so successful commands are not treated as failed only because they write to `stderr`.
- Updated installation, tutorial, and troubleshooting documentation.

## 2.1 - 2026-06-12

- Migrated inputs from `INPUT.py` to `input.toml`.

## 2.0 - 2026-06-08

- Updated code to support modern compute architectures including Python 3, Intel oneAPI LLVM compilers, and macOS.

## 1.2 - 2020-01-13

- Fixed exponentially large numbers in `UNI_mat.dat` for SCF calculations.

## 1.1 - 2020-05-11

- Added support for Quantum Espresso through AiiDA.

## 1.0 - 2020-04-23

- Cleaned repository.
- Defaulted to Python 2.x version.

## 0.3 - 2019-11-25

- Added `DMFT.py` and `postDMFT.py` scripts.

## 0.2 - 2019-07-10

- Added DMFTwDFT library version.

## 0.1 - 2018-07-31

- Initial release.
