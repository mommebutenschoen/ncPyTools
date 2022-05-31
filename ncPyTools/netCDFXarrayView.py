from xarray import open_dataset
try:
    ucstr = unicode  # python2
except NameError:
    ucstr = str  # python3
try:
    inpfunct = raw_input  # python2
except NameError:
    inpfunct = input  # python3

def ncXarrayView():
    """
    Main entry-point function using argument parser.

    Example:
        `netCDFXarrayView -h`
    """
    import argparse
    parser = argparse.ArgumentParser(
        description='Read netcdf files from command line into xarray.Dataset.')
    parser.add_argument(
        'filename', type=str, nargs='?',
        help='Filename of the netfdf file to open.'
        )
    parser.add_argument(
        '-q', '--quiet',
        help='Suppress header outputs.')
    args = parser.parse_args()
    filename = args.filename
    if not filename:
        filename = ucstr(inpfunct('Give netCDF file name: '))
    nc = open_dataset(filename)
    if not args.quiet: print(nc)
    return nc

if __name__ == "__main__":
    nc = ncXarrayView()
