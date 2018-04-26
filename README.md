[![Build Status](https://travis-ci.org/pyflowgo/pyflowgo.svg?branch=master)](https://travis-ci.org/pyflowgo/pyflowgo)

# Welcome to PyFLOWGO

Lava flow advance may be modeled through tracking the evolution of the lava's thermo-rheological properties, which are defined by viscosity and yield strength. These rheological properties evolve, in turn, with cooling and crystallization. Such model was conceived by Harris and Rowland (2001) who developed a 1-D model, FLOWGO, in which velocity of a control volume flowing down a channel depends on rheological properties computed following the lava cooling and crystallization path estimated via a heat balance box model. 

PyFLOWGO is an updated version of FLOWGO written in Python 3, that is open-source and compatible with any operating system.

**If you use PyFLOWGO please cite the following reference **:

"Chevrel M.O., Labroquère J., Harris A. and Rowland S. (2018). PyFLOWGO: an open-source platform for simulation of channelized lava thermo-rheological properties. Computers and Geosciences Vol. 111. p.167–180. https://doi.org/10.1016/j.cageo.2017.11.009"

This article contains an overview of the technical details in PyFLOWGO. You can also cite additional references for specific features and algorithms.

# Installation
This package needs a Python version >= 3.3.
Furthermore it uses numpy, scipy and matplotlib.

We recommend to use anaconda from Continuum with Python 3 which is availlable at: https://www.continuum.io/downloads

With anaconda, to install the environment named py3k containing Python 3 and the necessary packages, run in a shell:
```sh
$ conda create -n py3k python=3 anaconda
$ conda source py3k
```
That will activate the environment.

If you don't want to use anaconda, you can still use pip to install the necessary packages under Python 3:
```sh
$ pip install -r requirements.txt
```
You can then run the software using:
```sh
$ python3 main_flowgo.py ./resource/template.json
```
For further information, please read the PyFLOWGO_for_dummies.pdf file.

# Authors / developers

The PyFLOWGO main developers are:
   - Dr. Magdalena Oryaëlle Chevrel (oryaelle.chevrel@gmail.com) - Université Clermont Auvergne, CNRS, IRD, OPGC, Laboratoire Magmas et Volcans
   - Dr. Jérémie Labroquère (jeremie.labroquere@gmail.com) - https://www.linkedin.com/in/jlabroquere/

# License
The current license of the software is LGPL v3.0.
