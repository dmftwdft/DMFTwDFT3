import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "DMFTwDFT3"
copyright = "2026, The DMFTwDFT Project"
author = "Uthpala Herath"
release = "2.0"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
]

source_suffix = {
    ".md": "markdown",
}
root_doc = "index"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "dollarmath",
]

html_theme = "furo"
html_title = "DMFTwDFT3"
html_logo = "../docs/images/dmftwdft-hd.png"
html_static_path = []
html_theme_options = {
    "source_repository": "https://github.com/DMFTwDFT/DMFTwDFT3/",
    "source_branch": "master",
    "source_directory": "sphinx/",
}

htmlhelp_basename = "DMFTwDFT3doc"

latex_documents = [
    (root_doc, "DMFTwDFT3.tex", "DMFTwDFT3 Documentation", author, "manual"),
]

man_pages = [(root_doc, "dmftwdft3", "DMFTwDFT3 Documentation", [author], 1)]

texinfo_documents = [
    (
        root_doc,
        "DMFTwDFT3",
        "DMFTwDFT3 Documentation",
        author,
        "DMFTwDFT3",
        "DFT+DMFT framework documentation.",
        "Miscellaneous",
    ),
]
