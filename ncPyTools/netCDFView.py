from __future__ import print_function
from numpy import zeros
from netCDF4 import Dataset
from netCDF4 import num2date as n2d
import re
try:
    ucstr = unicode  # python2
except NameError:
    ucstr = str  # python3
try:
    inpfunct = raw_input  # python2
except NameError:
    inpfunct = input  # python3


class netCDFView(Dataset):
    """
    Class for quick inspection of netCDF files reading in a netCDF file
    into a netCDF4 object in read-only mode.
    """
    def __enter__(self,):
        return self

    def __init__(self, filename, Mask=True, Quiet=False):
        """
        Initialise netCDF4 object.

        Args:
            filename (str): Path to netCDF file.
            Mask (bool): Mask variables with their fill value.
            Quiet (bool): Suppress output of netCDF header information.
        """
        Dataset.__init__(self, filename, 'r')
        if Mask:
            for var in self.variables.values():
                var.set_auto_maskandscale(True)
        if not Quiet:
            print(self)

    def lon(self):
        """
        Try to extract longitude.

        Returns:
            Longitude variable data, `None` if unsuccessful.
        """
        Lon = None
        for key, var in self.variables.items():
            try:
                try:
                    lon = self.variables[key+'_bnds'][:]
                    if lon.shape[1] == 2:
                        Lon = zeros(lon.shape[0]+1)
                        Lon[:-1] = lon[:, 0]
                        Lon[-1] = lon[-1, 1]
                    else:
                        Lon = lon
                except:
                    Lon = var[:]
            except:
                pass
        return Lon

    def lat(self):
        """
        Try to extract latitude.

        Returns:
            Latitude variable data, `None` if unsuccessful.
        """
        Lat = None
        for key, var in self.variables.items():
            try:
                try:
                    lat = self.variables[key+'_bnds'][:]
                    if lat.shape[1] == 2:
                        Lat = zeros(lat.shape[0]+1)
                        Lat[:-1] = lat[:, 0]
                        Lat[-1] = lat[-1, 1]
                    else:
                        Lat = lat
                except:
                        Lat = var[:]
            except:
                pass
        return Lat

    def time(self):
        """
        Try to extract time.

        Returns:
            Time variable data, `None` if unsuccessful.
        """

        Time = None
        for key, Var in self.variables.items():
            if key in ('time', 'days', 'hours', 'minutes', 'seconds'):
                Time = Var[:]
            else:
                try:
                    # if this doesn't fail it's a time variable
                    Date = n2d(0, Var.units)
                    Time = Var[:]
                except:
                    pass
            return Time

    def dates(self):
        """
        Try to extract dates.

        Returns:
            Time variable as datetime object, `None` if unsuccessful.
        """

        Dates = None
        for key, Var in self.variables.items():
            if key == 'time':
                n2d(0, Var.units)
                if "calendar" in nc.variables["time"].ncattrs():
                    calstr=nc.variables["time"].calendar
                else:
                    calstr="standard"
                try:
                    Dates = n2d(Var[:], Var.units,calendar=calstr)
                except:
                    print("Couldn't find time variable with valid date units.")
        return Dates

    def __call__(self, varStr, Squeeze=True, Object=False):
        """Get netcdf variable.

        Args:
            varStr (str): Variable to extract.
            Squeeze (bool): Remove singleton dimensions.
            Object (bool): Return actual netCDF4 object (`True`) or variable
                or data (`False`).

        Returns:
            netCDF4 variable object or data.
        """
        if Object:
            return self.variables[varStr]
        else:
            if Squeeze:
                return self.variables[varStr][:].squeeze()
            else:
                return self.variables[varStr][:]

    def __unicode__(self):
        """netCDF file header in `reStructuredText` format."""
        try:
            objectname = self.filepath()
        except ValueError:
            objectname = "netCDF4 Object"
        barLength = len(objectname)
        # write filename as 1st level title:
        infoStr = u'=' * barLength + u'\n' +\
            objectname + u'\n' +\
            u'=' * barLength + u'\n\n\n'
        # write global attributes as 2nd level title:
        title = u'Global Attributes:'
        barLength = len(title)
        infoStr += u'#' * barLength + u'\n' +\
            title + '\n' +\
            u'#' * barLength + u'\n'
        for key in self.ncattrs():
            infoStr += u'\n'+key+u':\n   '
            attr = ucstr(self.getncattr(key))
            r = re.compile(r'\n')
            attr = r.sub(r'\n  ', attr)
            infoStr += ucstr(attr) + u'\n'
        infoStr += '\n\n'
        dimList = self.dimensions.items()
        dimList = [(key, dim, len(dim)) for key, dim in dimList]
        dimList.sort(key=lambda x: x[0])
        title = u'Dimensions:'
        barLength = len(title)
        infoStr += title + '\n' +\
            u'-' * barLength + u'\n'
        for key, dim, size in dimList:
            infoStr += u'\n' + key + u':'
            if dim.isunlimited():
                infoStr += u'\n   UNLIMITED => ' + ucstr(size)
            else:
                infoStr += u'\n   ' + ucstr(size)
        infoStr += u'\n\n'
        title = u'Variables:'
        barLength = len(title)
        infoStr += title + '\n' +\
            u'-' * barLength + u'\n'
        varList = list(self.variables.items())
        varList.sort(key=lambda x: x[0])
        for key, var in varList:
            infoStr += '\n'+key+':'
            metadata = {}
            for k in var.ncattrs():
                metadata[k] = ucstr(getattr(var, k))
            if 'long_name' in metadata.keys():
                infoStr += '\n  ' + ucstr(getattr(var, 'long_name'))
            if 'units' in metadata.keys():
                infoStr += u'\n  ' + '[' + ucstr(getattr(var, 'units')+']')
            infoStr += u'\n  ' + ucstr(var.dimensions) + '=' +\
                ucstr(var.shape)
            infoStr += u'\n  ' + ucstr(var.dtype)
        return infoStr

    def varInfo(self, varStr):
        """Extract variable metadata.

        Args:
            varStr (str): variable key.

        Returns:
            str: Variable meta data.
        """
        try:
            var = self.variables[varStr]
            infoStr = u'\n\t' + varStr + ucstr(var.dimensions) +\
                u': '+ucstr(var.shape) + u'\t'+ucstr(var.dtype)
            for k in var.ncattrs():
                infoStr += u'\n\t\t' + ucstr(k) + u':\t' +\
                    ucstr(getattr(var, k)) + u'\n'
            print(infoStr)
        except KeyError:
            print('Variable "' + varStr + '" not found!')

    def diff(self, varStr, refObj, refStr="", scaleFunction=0, relative=0):
        """Difference of variable to reference data from another netCDFView object.

        Args:
            refObj (netCDFView object): object containing the reference data.
                Must have the same geometry as the calling object.
            varStr (str): string identifying the variable to compare
            refStr (str): string of variable to compare in the reference object.
                Defaults to varStr.
            scaleFunction: function to scale reference data before comparison,
                taking a single argument of the type of the reference data and
                returning the same type and shape.
                By default no scaling is applied. Should return data of the same shape and type as
            relative(boolean): Flag to normalise differences.
                0, default - no normalisation
                1 - (scaled) reference data
                2 - 0.5*(variables data + (scaled) reference data)
        """
        if refStr:
            refData=refObj.variables[refStr][:]
        else:
            refData=refObj.variables[varStr][:]
        if scaleFunction: refData=scaleFunction(refData)
        delta=self.variables[varStr][:]-refData
        if relative:
            if relative==2:
                delta/=0.5*(self.variables[varStr][:]+refData)
            else:
                delta/=refdata
        return delta

    def __exit__(self, etype, evalue, tb):
        if tb is None:
            self.close()
        else:
            print("Exception type:", etype)
            print("Exception value:", evalue)
            print("Traceback:", tb)
            raise


def ncdfView():
    """
    Main entry-point function using argument parser.

    Example:
        `netCDFView -h`
    """
    import argparse
    parser = argparse.ArgumentParser(
        description='Read netcdf files from command line.')
    parser.add_argument(
        'filename', type=str, nargs='?',
        help='Filename of the netfdf file to open.'
        )
    parser.add_argument(
        '-o', '--object', action="store_true",
        help='Open file as pure netCDF4 object.')
    parser.add_argument(
        '-q', '--quiet',
        help='Suppress header outputs.')
    parser.add_argument(
        '-n', '--nomask',
        help="Don't mask fill values")
    args = parser.parse_args()
    filename = args.filename
    Mask = True
    if args.nomask:
        Mask = False
    if not filename:
        filename = ucstr(inpfunct('Give netCDF file name: '))
    nc = netCDFView(filename, Mask=Mask, Quiet=args.quiet)
    return nc


if __name__ == "__main__":
    nc = ncdfView()
