# MTG

[![Docs](https://readthedocs.org/projects/mtg/badge/?version=latest)](https://mtg.readthedocs.io/)
[![Build Status](https://github.com/openalea/mtg/actions/workflows/openalea_ci.yml/badge.svg)](https://github.com/openalea/mtg/actions/workflows/conda-package-build.yml?query=branch%3Amaster)
[![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License--CeCILL-C-blue)](https://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html)
[![Anaconda-Server Badge](https://anaconda.org/openalea3/openalea.mtg/badges/version.svg)](https://anaconda.org/openalea3/mtg)

Multiscale Tree Graph datastructure and interfaces

## Description

MTG (Multi-scale Tree Graph) is a common data structure to represent
plant architecture at various scales.

MTG package aims to define :

> -   A share data structure for plant architecture representation.
> -   Read and write MTG files.
> -   Export to various graph format.
> -   Several algorithms for MTG.

### Authors

> -   Christophe Pradal

### Institutes

CIRAD / INRAE / inria

### Status

Python package

### License

CecILL-C

## Installation

#### for user
```bash
    conda install -c openalea3 -c conda-forge openalea.mtg
```

#### for developer
```bash
mamba env create -f ./conda/environment.yml
```
