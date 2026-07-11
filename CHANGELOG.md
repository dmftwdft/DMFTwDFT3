# Changelog

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
