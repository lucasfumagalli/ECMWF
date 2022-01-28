from   mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib
from   netCDF4 import Dataset as Dataset
import numpy as np
from osgeo import gdal 
from mpl_toolkits.basemap import addcyclic
import numpy as np # Import the Numpy package
from numpy import linspace 
from numpy import meshgrid 
import matplotlib.patheffects as path_effects
import matplotlib.patheffects as path_effects
import scipy.ndimage as ndimage
import matplotlib.image as image
from scipy.ndimage.filters import minimum_filter, maximum_filter
import csv
import datetime as dt
import wget
from datetime import datetime
from datetime import date
from matplotlib.colors import LinearSegmentedColormap 
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.patheffects as path_effects
import sys
import pygrib
sys.stdout = open("VARS.txt", "w")
file = '20220127000000-15h-oper-fc.grib2'

grib = gdal.Open(file)
gr = pygrib.open(file)
for i in gr:
    print(i)




mensagem='arquivo aberto! Montado arquivo'
print(mensagem)

extent = [-56.4, -28, -45.9, -22]

min_lon = extent[0]; max_lon = extent[2]; min_lat = extent[1]; max_lat = extent[3]
grib = gdal.Translate('subsected_grib.grb', grib, projWin = [min_lon , max_lat, max_lon , min_lat])




mensagem='procurando variáveis'
print(mensagem)

n=1
print('concluido')


for item in range(82):
    print(n)
    dado = grib.GetRasterBand(n)
    metadata = dado.GetMetadata()
    band_name = metadata['GRIB_COMMENT']
    print(band_name)
    band_description = dado.GetDescription()
    print(band_description)
    n=n+1 
sys.stdout.close()   