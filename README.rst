
=========
ncPyTools
=========

Python tools for the handling of `netcdf` files based on the `python-netCDF4`
library.
These tools currently only support files of `netcdf` **classic** structure.


##############
Tools inlcuded
##############


ncdfView
--------

Simple python wrapper around the python-netCDF4 library to read `netcdf` files
from the command line.

Useage
^^^^^^

Help-string::

  ncdfView.py [-h] [-o] [-q QUIET] [-n NOMASK] [filename]

  Read netcdf files from command line.

  positional arguments:
    filename              Filename of the netfdf file to open.

  optional arguments:
    -h, --help            show this help message and exit
    -o, --object          Open file as pure netCDF4 object.
    -q QUIET, --quiet QUIET
                          Suppress header outputs.
    -n NOMASK, --nomask NOMASK
                          Don't mask fill values
In order to obatin an interactive prompt with the netcdf file loaded into a the `ncdfView` object called `nc`
launch::

  python3 -i -m ncPyTools.ncdfViewncPyTools.ncdfView

Installation:
^^^^^^^^^^^^^

After downloading the source from the repository install via pip, descend
into the top-level of the source tree
and launch::

  pip3 install .

or to install in developers mode::

  pip3 install -e .
