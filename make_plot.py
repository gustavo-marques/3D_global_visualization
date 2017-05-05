
import numpy as np
from ideal_ice_shelf_3D import *
from netCDF4 import Dataset
import pyvtk

# etopo
n = 10
topo = netCDF4.Dataset('etopo5.nc').variables['topo'][::n,::n]
lon = netCDF4.Dataset('etopo5.nc').variables['topo_lon'][::n] * np.pi/ 180.
lat = netCDF4.Dataset('etopo5.nc').variables['topo_lat'][::n] * np.pi/ 180.
jm,im = topo.shape
# scale topo
topo = topo/24000.
# masking
topo=np.ma.masked_where(topo == 0., topo)
topo.mask = np.ma.array(topo); topo.mask[:,:]=False
# Create a sphere
r = 0.3
pi = np.pi
cos = np.cos
sin = np.sin
#phi, theta = np.mgrid[0:pi:217j, 0:2 * pi:432j]
phi, theta = np.mgrid[0:pi:201j, 0:2 * pi:201j]
#phi, theta = np.meshgrid(lon,lat)
#x = r * sin(theta) * cos(phi)
x = r * sin(phi) * cos(theta)
#y = r * sin(theta) * sin(phi)
y = r * sin(phi) * sin(theta)
#z = (r+topo) * cos(theta)
#z = (r+topo) * cos(phi)
z = (r) * cos(phi)

topo = np.zeros((phi.shape))
topo=np.ma.masked_where(topo == 0., topo)
topo.mask = np.ma.array(topo); topo.mask[:,:]=False
jm,im = topo.shape

# this is just used for shape's porpuses
h = np.zeros((10,jm,im))
# generate bathymetry (VTK file)
#VTKgen(y,x,topo.mask,depth=z,h=h,fname='test')

newlat=np.resize(lat,(2,jm,im))
newlon=np.resize(lon,(2,jm,im))
newdepth,bottom=get_depth(h,z,topo.mask)
pp = f3(newlon,newlat,newdepth)
structure=pyvtk.StructuredGrid([2,jm,im],pp)
# create bottom/shape and depths
newdepth=f1(newdepth)
bottom=f1(bottom)
pointdata = pyvtk.PointData(pyvtk.Scalars(newdepth,name='Depth'), pyvtk.Scalars(bottom,name='Bottom9999'))
# saving the data
vtk = pyvtk.VtkData(structure,pointdata)
vtk.tofile('bathymetry','binary')
