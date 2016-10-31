#!/usr/bin/python
# -*- coding: latin-1 -*-

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


class ncdfView(Dataset):
    def __enter__(self,):
        return self

    def __init__(self, filename, Mask=True, Quiet=False):
        Dataset.__init__(self, filename, 'r')
        if Mask:
            for var in self.variables.values():
                var.set_auto_maskandscale(True)
        if not Quiet:
            print(self)

    def lon(self):
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
        Dates = None
        for key, Var in self.variables.items():
            if key == 'time':
                n2d(0, Var.units)
                try:
                    Dates = n2d(0, Var.units)
                    Dates = n2d(Var[:], Var.units)
                except:
                    pass
        return Dates

    def __call__(self, varStr, Squeeze=True, Object=False):
        if Object:
            return self.variables[varStr]
        else:
            if Squeeze:
                return self.variables[varStr][:].squeeze()
            else:
                return self.variables[varStr][:]

    def __unicode__(self):
        barLength = len(self.filepath())
        # write filename as 1st level title:
        infoStr = u'=' * barLength + u'\n' +\
            self.filepath() + u'\n' +\
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
            print(metadata.keys())
            if 'long_name' in metadata.keys():
                infoStr += '\n  ' + ucstr(getattr(var, 'long_name'))
            if 'units' in metadata.keys():
                infoStr += u'\n  ' + '[' + ucstr(getattr(var, 'units')+']')
            infoStr += u'\n  ' + ucstr(var.dimensions) + '=' +\
                ucstr(var.shape)
            infoStr += u'\n  ' + ucstr(var.dtype)
        return infoStr

    def varInfo(self, varStr):
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

    def __exit__(self, etype, evalue, tb):
        if tb is None:
            self.close()
        else:
            print("Exception type:", etype)
            print("Exception value:", evalue)
            print("Traceback:", tb)
            raise


def netCDFView():
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
    return ncdfView(filename, Mask=Mask, Quiet=args.quiet)


if __name__ == "__main__":
    nc = netCDFView()
