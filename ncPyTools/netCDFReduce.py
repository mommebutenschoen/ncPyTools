"""Collection of functions to reduce netcdf file sizes by reducing float precision."""

from netCDF4 import Dataset
from pathlib import Path

def netCDFRound(fname,vlist,digits,outpath="",Quiet=False):
    """ Rounds list of variables in input file to a given number of significant Xdigits.
    Writes to file in outpath with same name as input file, but inserting the .Xdigits
    suffix before the filetype suffix.

    Args:
            filename(str): input netcdf file including path
            vlist(list of str): list of variables to round
            digits(int): number of significant digits to keep
            outpath(str): path where to place reduced size file, defaults to the
                same path as input file
    """

    p=Path(fname)
    newsuffix="{}digits{}".format(digits,p.suffix)
    packedfile=file=p.parents[0] / "{}.{}".format(p.stem,newsuffix)
    if Quiet: print("Rounding variables {}...".format(vlist))
    with Dataset("{}".format(p)) as src, Dataset("{}".format(packedfile), "w") as dst:
        # copy global attributes all at once via dictionary
        dst.setncatts(src.__dict__)
        # copy dimensions
        for name, dimension in src.dimensions.items():
            dst.createDimension(
                name, (len(dimension) if not dimension.isunlimited() else None))
        # copy all file data except for the excluded
        for name, variable in src.variables.items():
            attributes=src[name].__dict__
            fv=attributes.pop("_FillValue",None)
            if name not in vlist:
                if fv is None:
                    x = dst.createVariable(name,variable.datatype,variable.dimensions)
                else:
                    x = dst.createVariable(name,variable.datatype,variable.dimensions,fill_value=fv)
            else:
                if Quiet: print("Rounding {}...".format(name))
                if fv is None:
                    x = dst.createVariable(name, 'f4',variable.dimensions,zlib=True,complevel=9,least_significant_digit=digits)
                else:
                    x = dst.createVariable(name, 'f4',variable.dimensions,zlib=True,complevel=9,least_significant_digit=digits,fill_value=fv)
            dst[name][:] = src[name][:]
            # copy variable attributes all at once via dictionary
            dst[name].setncatts(attributes)
    if Quiet: print("Done.")

def netCDFPack(fname,vlist,outpath="",Quiet=False):
    """ Packs list of variables in input file into 16bits integers with scale and offset.
    Writes to file in outpath with same name as input file, but inserting the .Xdigits
    suffix before the filetype suffix.

    Args:
            filename(str): input netcdf file including path
            vlist(list of str): list of variables to round
            outpath(str): path where to place reduced size file, defaults to the
                same path as input file
            Quiet(bool): if False print log messages, otherwise operate quietly
    """

    p=Path(fname)
    newsuffix="16bits{}".format(p.suffix)
    packedfile=file=p.parents[0] / "{}.{}".format(p.stem,newsuffix)
    if Quiet: print("Packing variables {}...".format(vlist))
    with Dataset("{}".format(p)) as src, Dataset("{}".format(packedfile), "w") as dst:
        # copy global attributes all at once via dictionary
        dst.setncatts(src.__dict__)
        # copy dimensions
        for name, dimension in src.dimensions.items():
            dst.createDimension(
                name, (len(dimension) if not dimension.isunlimited() else None))
        # copy all file data except for the excluded
        for name, variable in src.variables.items():
            attributes=src[name].__dict__
            fv=attributes.pop("_FillValue",None)
            if name not in vlist:
                if fv is None:
                    x = dst.createVariable(name,variable.datatype,variable.dimensions)
                else:
                    x = dst.createVariable(name,variable.datatype,variable.dimensions,fill_value=fv)
            else:
                if Quiet: print("Packing {}...".format(name))
                offset=data.min()
                scale=(data.max()-offset)
                if fv is None:
                    x = dst.createVariable(name, 'u2',variable.dimensions,zlib=True,complevel=9)
                    scale/=(2**bits-1) # scale data from 0 to 2**bits -1
                else:
                    fv=2**bits-1 # Fill Value is maximum integer
                    x = dst.createVariable(name, 'u2',variable.dimensions,zlib=True,complevel=9,fill_value=fv)
                    scale/=(2**bits-2)  # scale data from 0 to 2**bits -2
                idata = (.5+(data-offset)/scale).astype('u2')
                if fv is None:
                    dst[name][:]=idata
                else:
                    dst[name][:]=where(data[:].mask,fv,idata)
                    dst[name].add_offset=offset
                    dst[name].scale_factor=scale
            # copy variable attributes all at once via dictionary
            dst[name].setncatts(attributes)
    if Quiet: print("Done.")
