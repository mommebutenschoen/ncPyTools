#!/usr/bin/python
# -*- coding: latin-1 -*-

from __future__ import print_function
from sys import argv
from os import listdir, getcwd
from numpy import zeros
from netCDF4 import Dataset
from netCDF4 import num2date as n2d


class ncdfView(Dataset):
    def __enter__(self,):
        return self

    def __init__(self, filename, Mask=True, Quiet=False):
        if not Quiet:
            print('Opening nCDF-file %s ...' % filename)
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
                if var.units == 'degrees_east':
                    print("...extracting longitude...")
                try:
                    lon = self.variables[key+'_bnds'][:]
                    if lon.shape[1] == 2:
                        Lon = zeros(lon.shape[0]+1)
                        Lon[:-1] = lon[:, 0]
                        Lon[-1] = lon[-1, 1]
                        print("bnd")
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
                if var.units == 'degrees_north':
                    print("...extracting latitude...")
                try:
                    lat = self.variables[key+'_bnds'][:]
                    if lat.shape[1] == 2:
                        Lat = zeros(lat.shape[0]+1)
                        Lat[:-1] = lat[:, 0]
                        Lat[-1] = lat[-1, 1]
                        print("bnd")
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
                print("...found ", key, "...")
                Time = Var[:]
            else:
                try:
                    # if this doesn't fail it's a time variable
                    Date = n2d(0, Var.units)
                    Time = Var[:]
                    print("...found ", key, "...")
                except:
                    pass
            return Time

    def dates(self):
        Dates = None
        for key, Var in self.variables.items():
            if key=='time':
                print("...found ", key, "...")
                n2d(0, Var.units)
                try:
                    Dates = n2d(0, Var.units)
                    print("...found ", key, Var.units, "...")
                    print("Reference date of time variable: ", Dates)
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
        infoStr = u'-----------------\n' +\
            u'netCDF Object:\n' +\
            u'-----------------'
        for key in self.ncattrs():
            infoStr += u'\n\n'+key+u':\t'
            infoStr += unicode(self.getncattr(key))
        dimList = self.dimensions.items()
        dimList = [(key, dim, len(dim)) for key, dim in dimList]
        dimList.sort(key=lambda x: x[0])
        for key, dim, size in dimList:
            infoStr += u'\n\t'+key
            if dim.isunlimited():
                infoStr += u'\tUNLIMITED => ' + unicode(size)
            else:
                infoStr += u'\t' + unicode(size)
        infoStr += u'\n\n'+u'Variables:\n'
        varList = list(self.variables.items())
        varList.sort(key=lambda x: x[0])
        for key, var in varList:
            print(key)
            infoStr += '\n\t'+key+':'
            for k in var.ncattrs():
                if k == 'long_name':
                    infoStr += u'\t' + unicode(getattr(var, k))
                elif k == 'units':
                    infoStr += u'\t' + '[' + unicode(getattr(var, k)+']')
            infoStr += u'\n\t\t' + unicode(var.dimensions) + '=' +\
                unicode(var.shape)
            infoStr += u'\t' + unicode(var.dtype)
        return infoStr

    def varInfo(self, varStr):
        try:
            var = self.variables[varStr]
            infoStr = u'\n\t' + varStr + unicode(var.dimensions) +\
                u': '+unicode(var.shape) + u'\t'+unicode(var.dtype)
            for k in var.ncattrs():
                infoStr += u'\n\t\t' + unicode(k) + u':\t' +\
                    unicode(getattr(var,k)) + u'\n'
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

if __name__ == "__main__":
    fn = None
    Mask = True
    if len(argv) < 2:
        print(str([el for el in listdir(getcwd()) if el[-3:] == '.nc']))
        filename = input('Give netCDF file name: ')
    else:
        for arg in argv[1:]:
            if arg == '-nm':
                Mask = False
            else:
                filename = argv[1]
    if not filename:
        print(str([el for el in listdir(getcwd()) if el[-3:] == '.nc']))
        filename = input('Give netCDF file name: ')
    nc = ncdfView(filename)
    print('created ncdf Object nCDF.')
