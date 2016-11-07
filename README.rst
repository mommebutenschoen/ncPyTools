
================
ncPyTools README
================

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


netCDFTemplate:
---------------

Useage
^^^^^^

Help-string::

  usage: netCDFTemplate [-h] [-c COMPRESS] yamlfile

  Create netcdf file from yaml metadata.

  positional arguments:
    yamlfile              yaml metadata file.

  optional arguments:
    -h, --help            show this help message and exit
    -c COMPRESS, --compress COMPRESS
                          Compression level (0 = no compression, 9 = maximum
                          compression)

Example `yaml` metadata file::

  filename: month_flux_2006c.nc
  dimensions:
      t: None
      y: 45
      x: 72
  unlimited_shape:
      t: 12
  variables:
      LAT:
          long_name: latitude
          units: degrees_north
          value: 1.e12
          fill_value: 1.e12
          dimensions: y
          type: f4
      LON:
          long_name: longitude
          units: degrees_east
          value: 1.e12
          fill_value: 1.e12
          dimensions: x
          type: f4


Installation:
-------------

After downloading the source from the repository install via pip, descend
into the top-level of the source tree
and launch::

  pip3 install .

or to install in developers mode::

  pip3 install -e .
