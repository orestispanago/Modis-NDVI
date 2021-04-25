import xarray as xr 
import numpy as np
import datetime
import os
import glob
import geopandas
import rioxarray
from shapely.geometry import mapping
from numpy import newaxis

hdf_files = glob.glob("modis/*.hdf")
shp = geopandas.read_file('shapefiles/GRC_adm3.shp')

#generate the Lat and Lon for 0.1x0.1 
lats = np.linspace(90, -90, 3600)
lats = np.round(lats, 2)
lons = np.linspace(-180, 180, 7200)
lons = np.round(lons, 2)
    
def get_datetime(base_name):
    yyd = base_name.split(".")[1][1:]
    return datetime.datetime.strptime(yyd, "%Y%j")

for hdf_file in hdf_files:   
    base_name = os.path.basename(hdf_file)
    ds = xr.open_dataset(hdf_file)
    ndvi = ds['CMG 0.05 Deg Monthly NDVI']/100000000
    
    date_dim = get_datetime(base_name)
    values = ndvi.values[:,:, newaxis]
    
    dsa = xr.DataArray(values,
                       name="NDVI", 
                       dims=["y","x",'time'], 
                       coords=[lats, lons, [date_dim]])
    
    dsa = dsa.rio.set_crs(4326)
    clipped = dsa.rio.clip(shp.geometry.apply(mapping), shp.crs)
    clipped.to_netcdf(f'clipped/{base_name[:-4]}.nc')

filenames = glob.glob('clipped/*.nc')
ds_all = xr.open_mfdataset(filenames, combine='by_coords')
ds_all = ds_all.load()
ds_all.to_netcdf('clipped/all_years.nc')