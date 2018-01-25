# Pykeeb

## Introduction
Pykeeb is a python 3 library that provides functions which can be used to generate MX or ALPS keyswitch plates with ease and flexibility.  Ortholinear and staggered (untested) switch matrices can be generated given a number of columns and rows, before editing modifiers for individual rows, columns, or keys.  Arcs be generated as well, given a length and angle.  A projection function allows the plates to include walls, creating a self-supporting plate which can be exported from OpenSCAD and then 3d-printed.  Pykeeb is very alpha at this time - some manual work is also required to combine any separate arcs and/or matrices, **so please understand YMMV**.  Switch and keycap inclusion functions are useful to help visually detect collisions before printing.  For more info, please see my reference project and custom keyboard, the [PyErgo60](https://github.com/raycewest/pyergo60).

## Install
```# pip install pykeeb```


## Dependencies
[OpenPySCAD](https://github.com/taxpon/openpyscad) - Python lib to generate [OpenSCAD](https://www.openscad.org) code.  **don't install from the PyPI (pip), it's out of date** - download the tar.gz, then ```# pip install openpyscad-master.tar.gz```.

## License
MIT
