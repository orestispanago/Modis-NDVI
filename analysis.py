import xarray as xr 
import numpy as np
import datetime
import os
import glob
import geopandas
import rioxarray
from shapely.geometry import mapping

hdf_files = glob.glob("modis/*.hdf")

# ss = xr.open_dataset(hdf_files[0])
# rds = rioxarray.open_rasterio("raw/MOD13C2.A2010001.006.2015198205120.hdf")

# var = ss.variables
# yyd = hdf_files[0].split("/")[1].split(".")[1][1:]

# year_day = datetime.datetime.strptime(yyd, "%Y%j")


ds = xr.open_dataset('modis/MOD13C2.A2010001.006.2015198205120.hdf')

ndvi = ds['CMG 0.05 Deg Monthly NDVI']/100000000


#generate the Lat and Lon for 0.1x0.1 
lats = np.linspace(90, -90, 3600)
lats = np.round(lats, 2)
lons = np.linspace(-180, 180, 7200)
lons = np.round(lons, 2)


dsa = xr.DataArray(ndvi.values, 
                   name="NDVI", 
                   dims=["y","x"], 
                   coords=[lats,lons])
# dsa.plot()



shp = geopandas.read_file('shapefiles/GRC_adm3.shp')

dsa = dsa.rio.set_crs(4326)
clipped = dsa.rio.clip(shp.geometry.apply(mapping), shp.crs)
clipped.plot(vmin=0)
