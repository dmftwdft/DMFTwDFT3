# DMFTwDFT3

DMFTwDFT is an open-source, user-friendly framework to calculate electronic, vibrational and elastic properties in strongly
correlated materials (SCM) using beyond-DFT methods such as DFT+U, DFT+Hybrids and DFT+DMFT (Dynamical Mean Field Theory) with a variety of different DFT codes. Currently supports VASP, Siesta and Quantum Espresso.

![](docs/images/dmftwdft-hd.png)

## Features <br />

![](docs/images/welcome.jpg)

## Workflow <br />

![](docs/images/steps.png)

## Installation and usage

Please refer to the documentation.

https://dmftwdft.github.io/DMFTwDFT3/

**Quick Install:**

Copy one of the templates in `config` to `Makefile.in` in the repo root, edit it for your machine, and run the setup.:

E.g.,

```bash
cp config/Makefile.in.gnu Makefile.in
python setup.py
```

Available templates:

- `config/Makefile.in.gnu`: GNU compilers on Linux-style systems.
- `config/Makefile.in.intel`: Intel oneAPI compilers.
- `config/Makefile.in.mac`: macOS conda environment using GNU Fortran, MPI, BLAS/LAPACK, GSL and FFTW from the same conda environment.

Recommended environments:

- Linux: `mamba env create -f environment.yml`
- macOS: `mamba env create -f environment.macos.yml`

**Notes:**

- For GNU compilers, it is assumed that `liblapack.a`, `libblas.a` and GSL libraries are installed in the `/usr/local/lib/` directory. If not, modify `LALIB` and `GSLLIB` in `Makefile.in` to point to the correct location. Additionally, set compiler flags in `FFLAGSEXTRA`.

- Keep every compiled component on the same architecture. On Apple Silicon, the provided `environment.macos.yml` creates a native `arm64` environment and `config/Makefile.in.mac` defaults to the native architecture. Build Wannier90, DMFTwDFT and any DFT interfaces against the same conda environment. Do not mix an `x86_64` Wannier90 binary with `arm64` conda BLAS/MPI libraries, or the reverse.

- For Intel builds on Linux, the Python environment still comes from `environment.yml`; only the Fortran/MPI compiler stack is external and should come from your Intel oneAPI module or shell setup.

## Developers

Hyowon Park <br />
Aldo Romero <br />
Uthpala Herath <br />
Vijay Singh <br />
Benny Wah <br />
Xingyu Liao <br />

## Contributors

Kristjan Haule <br />
Chris Marianetti <br />

## How to cite

If you have used DMFTwDFT in your work, please cite:

[DMFTwDFT: An Open-Source Code Combining Dynamical Mean Field Theory with Various Density Functional Theory Packages. Singh, V., Herath, U., Wah, B., Liao, X., Romero, A. H., and Park, H. Computer Physics Communications, 261: 107778. April 2021.](https://www.sciencedirect.com/science/article/abs/pii/S001046552030388X)

BibTex:

    @article{SINGH2021107778,
    title = "DMFTwDFT: An open-source code combining Dynamical Mean Field Theory with various density functional theory packages",
    journal = "Computer Physics Communications",
    volume = "261",
    pages = "107778",
    year = "2021",
    issn = "0010-4655",
    doi = "https://doi.org/10.1016/j.cpc.2020.107778",
    url = "http://www.sciencedirect.com/science/article/pii/S001046552030388X",
    author = "Vijay Singh and Uthpala Herath and Benny Wah and Xingyu Liao and Aldo H. Romero and Hyowon Park",
    keywords = "DFT, DMFT, Strongly correlated materials, Python, Condensed matter physics, Many-body physics",
    }

## Mailing list

Please post your questions on our forum: https://groups.google.com/d/forum/dmftwdft

## Acknowledgements

We acknowledge the use of the following packages:

- [Continuous time Quantum Monte Carlo (ctqmc)](http://hauleweb.rutgers.edu/tutorials/Tutorial0.html) through the eDMFT library.<br />

The original implementation of the CTQMC solver is described in the following paper:

[1] Kristjan Haule, Phys. Rev. B 75, 155113 (2007).

Free energy implementation :<br />
[2] Kristjan Haule, Turan Birol, Phys. Rev. Lett. 115, 256402 (2015).

- [Wannier90](http://www.wannier.org/)<br>
  Wannier90 as a community code: new features and applications, G. Pizzi et al., J. Phys. Cond. Matt. 32, 165902 (2020)

## Changelog

v2.0 June 8, 2026 - Updated code to support modern compute architectures including Intel oneAPI LLVM compilers and MacOS.<br />
v1.2 Jan 13th, 2020 - Fixed bug with exponentially large numbers in UNI_mat.dat for SCF calculations. <br />
v1.1 May 11th, 2020 - Added support for Quantum Espresso through Aiida. <br />
v1.0 April 23, 2020 - Cleaned repository. Defaulted to Python 2.x version. <br />
v0.3 November 25, 2019 - Added DMFT.py and postDMFT.py scripts <br />
v0.2 July 10, 2019 - DMFTwDFT library version <br />
v0.1 July 31, 2018 - Initial release (Command line version)
