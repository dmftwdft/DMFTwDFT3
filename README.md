# DMFTwDFT3

DMFTwDFT is an open-source, user-friendly framework to calculate properties of strongly correlated materials (SCM) using DMFT (Dynamical Mean Field Theory) with a variety of different DFT codes. Currently supports VASP, Siesta, and Quantum Espresso.

Read the documentation to learn more: https://dmftwdft.github.io/DMFTwDFT3

> [!NOTE]
> DMFTwDFT3 brings major updates to its Python-2 predecessor, [DMFTwDFT](https://github.com/dmftwdft/DMFTwDFT), with a focus on supporting modern compute architectures including a Python-3 ecosystem, Intel oneAPI LLVM compilers, and MacOS compatibility. Hereafter, DMFTwDFT3 will be referred to as DMFTwDFT for brevity.

![](docs/source/_static/images/dmftwdft-hd.png)

## Features <br />

![](docs/source/_static/images/welcome.jpg)

## Workflow <br />

![](docs/source/_static/images/steps.png)

## Quick Install

1\. Create a Python environment using a recommended `environment.yml` file.

- Linux: `mamba env create -f environment.yml`
- macOS: `mamba env create -f environment.macos.yml`

2\. Copy a build template to the repository root as `Makefile.in` and edit values as needed for your system.

- `config/Makefile.in.gnu`: GNU compilers on Linux-style systems.
- `config/Makefile.in.intel`: Intel oneAPI compilers.
- `config/Makefile.in.mac`: macOS Apple Silicon/Homebrew OpenMPI build using Homebrew compilers/MPI/OpenBLAS and conda-provided Python/GSL where configured.

3\. Run the setup script,

```bash
python setup.py
```

## Usage

Copy the DFT inputs (see [examples](https://github.com/dmftwdft/DMFTwDFT3/tree/master/examples)) along with an `input.toml` file to a working directory and run,

```shell
DMFT.py dmft --dft <dft_code> --structure-name <name_of_structure>
```

E.g., for SrVO3 with Siesta,

```shell
DMFT.py dmft --dft siesta --structure-name SrVO3
```

Afterwards, for post-processing run,

```shell
postDMFT.py ac --average 4
postDMFT.py dos
postDMFT.py bands --plot-plain
```

Refer to the [documentation](https://dmftwdft.github.io/DMFTwDFT3) to learn more about using DMFTwDFT and its features.

## Developers

- Hyowon Park (University of Illinois at Chicago)
- Aldo Romero (West Virginia University)
- Uthpala Herath (Duke University, West Virginia University)
- Vijay Singh (GITAM School of Science, University of Illinois at Chicago)
- Benny Wah (University of Illinois at Chicago)
- Xingyu Liao (University of Illinois at Chicago)

## Contributors

- Kristjan Haule (Rutgers University)
- Chris Marianetti (Columbia University)
- Javier Junquera (Universidad de Cantabria)

## How to cite

If you have used DMFTwDFT in your work, please cite,

V. Singh, U. Herath, B. Wah, X. Liao, A. H. Romero, and H. Park,
"DMFTwDFT: An open-source code combining Dynamical Mean Field Theory with various density functional theory packages,"
Computer Physics Communications 261, 107778 (2021).
[https://doi.org/10.1016/j.cpc.2020.107778](https://doi.org/10.1016/j.cpc.2020.107778)

BibTex,

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

We acknowledge the use of the following packages,

[Continuous time Quantum Monte Carlo (ctqmc)](http://hauleweb.rutgers.edu/tutorials/Tutorial0.html) through the eDMFT library.<br />

[1] Kristjan Haule, Phys. Rev. B 75, 155113 (2007). <br />
[2] Kristjan Haule, Turan Birol, Phys. Rev. Lett. 115, 256402 (2015).

[Wannier90](http://www.wannier.org/)<br>

[1] Wannier90 as a community code: new features and applications, G. Pizzi et al., J. Phys. Cond. Matt. 32, 165902 (2020)

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
