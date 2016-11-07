from __future__ import print_function
from netCDF4 import Dataset
from yaml import load
from argparse import ArgumentParser
from numpy import ones


class netCDFTemplate:
    """
    Class for generating netcdf templates.
    This class is mainly intended for the easy generation of netcdf files with
    a data layout defined in yaml metadata files, that are then to be filled
    with actual data.
    """

    def __init__(self, yamlfile):
        """
        Initialise a netCDFTemplate objerct with the yaml file that describes
        the data structure.

        Args:
            yamlfile (str): `yaml` file describing data structure.
        """
        print("Loading {}".format(yamlfile))
        D = self._loadYaml(yamlfile)
        self._setAttributes(D)

    def __call__(self, compress=5):
        """Writes the template object to a file.
        The optional `compress` keyword provides the compression level to be
        used for all variables.

        Args:
            compress (int): compression level to be used for all variables.
        """
        self._writeNCDF(compress=compress)

    def _writeNCDF(self, compress=5):
        nc = Dataset(self.filename, mode="w")
        print("Creating {}".format(self.filename))
        if hasattr(self, "global_attributes"):
            nc.setncatts(self.global_attributes)
        for k, v in self.dimensions.items():
            try:
                n = int(v)
            except TypeError:
                n = None
                print("\tDimension {} is UNLIMITED.".format(k))
            else:
                if n <= 0:
                    n = None
                    print("\tDimension {} UNLIMITED.".format(k))
            nc.createDimension(k, n)
        for k, v in self.variables.items():
            if v["dimensions"]:
                dims = v["dimensions"].split(",")
            else:  # if dimensions undefined define as scalar
                dims = ()
                print("\tVariables {} is scalar.".format(k))
            if "fill_value" in v.keys():
                nc.createVariable(k, v["type"], dims, zlib=compress,
                                  complevel=compress,
                                  fill_value=float(v["fill_value"]))
            else:
                nc.createVariable(k, v["type"], dims, zlib=compress,
                                  complevel=compress)
            nc.variables[k].long_name = v["long_name"]
            nc.variables[k].units = "{}".format(v["units"])
        for k, v in self.variables.items():
            if v["type"][0] == "f":
                conv = float
            elif v["type"][0] == "i":
                conv = int
            if v["dimensions"]:
                Shape = [self.shape[d] for d in v["dimensions"].split(",")]
                Slice = [slice(None, self.shape[d])
                         for d in v["dimensions"].split(",")]
                data = self.variables[k]["value"]
                if type(data) in (type(0.), type(0)):
                    nc.variables[k][Slice] = ones(Shape)*conv(
                        self.variables[k]["value"])
                else:
                    nc.variables[k][Slice] = data
            else:  # if dimensions undefined define as scalar
                nc.variables[k][:] = conv(
                    self.variables[k]["value"])
        nc.close()
        print("Done.")

    def _loadYaml(self, yamlfile):
        with open(yamlfile) as fid:
            D = load(fid)
        return D

    def _setAttributes(self, D):
        self.dimensions = D["dimensions"]
        self.shape = {}
        for el in self.dimensions:
            if self.dimensions[el] == "None":
                self.dimensions[el] = None
                self.shape[el] = int(D["unlimited_shape"][el])
            else:
                self.dimensions[el] = int(self.dimensions[el])
                self.shape[el] = self.dimensions[el]
        self.variables = D["variables"]
        self.filename = D["filename"]
        if "global_attributes" in D.keys():
            self.global_attributes = D["global_attributes"]


def ncdfTemplate():
    """
    Main entry-point function using argument parser.

    Example:
        `netCDFView -h`
    """
    parser = ArgumentParser(
        description='Create netcdf file from yaml metadata.')
    parser.add_argument(
        'yamlfile', type=str,
        help='yaml metadata file.'
        )
    parser.add_argument(
        '-c', '--compress', type=int,
        help='Compression level (0 = no compression, 9 = maximum compression)')
    args = parser.parse_args()
    nc = netCDFTemplate(args.yamlfile)
    nc(compress=args.compress)
    return nc

if __name__ == "__main__":
    ncdfTemplate()
