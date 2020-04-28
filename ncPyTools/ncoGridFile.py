from numpy import array2string
import logging

class gridfile:
    """Python class for nco gridfile."""

    def __init__(self,lon,lat,lon_bounds,lat_bounds,nvertex=4,type="curvilinear"):
        """Defines grid.

        Args:
            lon (numpy float array [j,i]): array with longitudinal cell coordinates, for
                curvilinear coordinates should have the longitudinal dimension as
                second dimension, latitudinal first
            lat (numpy float array [j,i]): array with latitudinal cell coordinates, for
                curvilinear coordinates should have the longitudinal dimension as
                second dimension, latitudinal first
            lon_bounds (numpy float array [j,i,nvertex]): array with vertex
                longitudinal coordinates, counterclockwise
            lat_bounds (numpy float array [j,i,nvertex]): array with vertex
                latitudinal coordinates, counterclockwise
            nvertex (integer): number of vertex points, forced to 4 for curvilinear
                grids
            type (string): type of grid, "curvilinear" or "unstructured"
        """

        self.lon=lon
        self.lat=lat
        self.lon_bounds=lon_bounds
        self.lat_bounds=lat_bounds
        if type=="curvilinear":
            self.type=type
            self.nvertex=4
        else:
            self.type="unstructured"
            self.nvertex=nvertex
        self.gridsize=self.lon.size
        self.xsize=self.lon.shape[1]
        self.ysize=self.lon.shape[0]

    def __call__(self,fid=False):
        """Generates gridfile string.

        Args:
            fid(TextIOWrapper): if present, TextIOWrapper to write gridfile inspection

        Returns:
            gridfile string if fid argument is not present
        """

        if fid:
            fid.write("gridfile = {}\n".format(self.type))
            fid.write("gridsize = {}\n".format(self.gridsize))
            fid.write("xsize = {}\n".format(self.xsize))
            fid.write("ysize = {}\n".format(self.ysize))
            fid.write("nvertex = {}\n".format(self.nvertex))
            fid.write("\n#Longitudes\n")
            for l in self.lon:
                fid.write(array2string(l,separator=" ",max_line_width=65536)[1:-1]+"\n")
            fid.write("\n#Longitudes of cell corners\n")
            for l in self.lon_bounds.reshape([-1,4]):
                fid.write(array2string(l,separator=" ")[1:-1]+"\n")
            fid.write("\n#Latitudes\n")
            for l in self.lat:
                fid.write(array2string(l,separator=" ",max_line_width=65536)[1:-1]+"\n")
            fid.write("\n#Latitudes of cell corners\n")
            for l in self.lat_bounds.reshape([-1,4]):
                fid.write(array2string(l,separator=" ")[1:-1])
        else:
            gridfile="gridfile = {}\n".format(self.type)
            gridfile+="gridsize = {}\n".format(self.gridsize)
            gridfile+="xsize = {}\n".format(self.xsize)
            gridfile+="ysize = {}\n".format(self.ysize)
            gridfile+="nvertex = {}\n".format(self.nvertex)
            gridfile+="\n#Longitudes\n"
            for l in self.lon:
                gridfile+=array2string(l,separator=" ",max_line_width=65536)[1:-1]+"\n"
            gridfile+="\n#Longitudes of cell corners\n"
            for l in self.lon_bounds.reshape([-1,4]):
                gridfile+=array2string(l,separator=" ")[1:-1]+"\n"
            gridfile+="\n#Latitudes\n"
            for l in self.lat:
                gridfile+=array2string(l,separator=" ",max_line_width=65536)[1:-1]+"\n"
            gridfile+="\n#Latitudes of cell corners\n"
            for l in self.lat_bounds.reshape([-1,4]):
                gridfile+=array2string(l,separator=" ")[1:-1]
            logging.info("Gridfile: ",gridfile)
            return gridfile
