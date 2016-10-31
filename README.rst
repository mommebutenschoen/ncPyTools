
=========
ncPyTools
=========

Python tools for the handling of `netcdf` files based on the `python-netCDF4`
library.


##############
Tools inlcuded
##############


--------
ncdfView
--------

Simple python wrapper around the python-netCDF4 library to read `netcdf` files
from the command line.

Help string::

  usage: ncdfView.py [-h] [-o] [-q QUIET] [-n NOMASK] [filename]

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
