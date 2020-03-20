import os, sys
from pathlib import Path
from mom6_tools.MOM6grid import MOM6grid
from mom6_tools.latlon_analysis import time_mean_latlon
from mom6_tools.m6plot import xyplot
import matplotlib.pyplot as plt
import warnings
import xarray as xr
import numpy as np
import argparse
class args:
  pass

# required arg
parser = argparse.ArgumentParser()
parser.add_argument('-grid', required=True, help='grid/geometry filename: ocean_geometry.nc')
parser.add_argument('-data', nargs='*', type=str, required=True, help='diag data filename(s): ocn*.nc or incr.1.nc')
parser.add_argument('-run_type',required=True, help='Type of run to plot: ana, fcst or incr')
parser.add_argument('-figs_path',help='path to save png files: ./fcst')
args = parser.parse_args()

print(f'Loading grid... {args.grid}')
print(f'Loading data... {args.data}')

if args.figs_path is None:
    print('Creating figures in -data directory ...')
else:
    if not os.path.isdir(args.figs_path): os.makedirs(args.figs_path)

grd= MOM6grid(args.grid)

# fcst & analysis
clim_sst=[-2,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32]
clim_ssh=[-1.8,-1.6,-1.4,-1.2,-1.0,-0.8,-0.6,-0.4,-0.2,0,0.2,0.4,0.6,0.8,1.0,1.2,1.4]
clim_sss=[30,31,32,33,34,35,36,37,38,39,40]
# Increments
clim_sst_incr=[-1.0,-0.8,-0.6,-0.4,-0.2,0,0.2,0.4,0.6,0.8,1.0]
clim_ssh_incr=[-0.5,-0.4,-0.3,-0.2,-0.1,0,0,0.1,0.2,0.3,0.4,0.5]
clim_sss_incr=[-1.0,-0.8,-0.6,-0.4,-0.2,0,0.2,0.4,0.6,0.8,1.0]

for filename in args.data:
    if (args.run_type == 'ana'):
        nc = xr.open_mfdataset(filename , decode_times=False)
        path_ = Path(filename)
        name_ = Path(filename).name
        if args.figs_path is None:
           sst_fig = str(path_.parent.joinpath(path_.stem + '_SST_ana.png'))
           ssh_fig = str(path_.parent.joinpath(path_.stem + '_SSH_ana.png'))
           sss_fig = str(path_.parent.joinpath(path_.stem + '_SSS_ana.png'))
        else:
           sst_fig = str(args.figs_path+'/'+path_.stem + '_SST_ana.png')
           ssh_fig = str(args.figs_path+'/'+path_.stem + '_SSH_ana.png')
           sss_fig = str(args.figs_path+'/'+path_.stem + '_SSS_ana.png')

        title_sst='SST analysis (degC):'+str(name_)
        title_ssh='SSH analysis (m):'+str(name_)
        title_sss='SSS analysis (psu):'+str(name_)

        Temp=nc.Temp.where(nc.Temp[0,0,:,:] !=0)
        xyplot(Temp[0,0,:,:].to_masked_array(),grd.geolon,grd.geolat,clim=clim_sst,title=title_sst,save=sst_fig)
        Salt=nc.Salt.where(nc.Salt[0,0,:,:] !=0)
        xyplot(Salt[0,0,:,:].to_masked_array(),grd.geolon,grd.geolat,clim=clim_sss,title=title_sss,save=sss_fig)
        ave_ssh=nc.ave_ssh.where((nc.ave_ssh[0,:,:] !=0) & (nc.ave_ssh[0,:,:] !=0.07500000000000014))
        xyplot(ave_ssh[0,:,:].to_masked_array(),grd.geolon,grd.geolat,clim=clim_ssh,title=title_ssh,save=ssh_fig)
        plt.close('all')
    
    elif (args.run_type == 'fcst'):
        nc = xr.open_mfdataset(filename , decode_times=False)
        path_ = Path(filename)
        name_ = Path(filename).name
        if args.figs_path is None:
           sst_fig = str(path_.parent.joinpath(path_.stem + '_SST_fcst.png'))
           ssh_fig = str(path_.parent.joinpath(path_.stem + '_SSH_fcst.png'))
           sss_fig = str(path_.parent.joinpath(path_.stem + '_SSS_fcst.png'))
        else:
           sst_fig = str(args.figs_path+'/'+path_.stem + '_SST_fcst.png')
           ssh_fig = str(args.figs_path+'/'+path_.stem + '_SSH_fcst.png')
           sss_fig = str(args.figs_path+'/'+path_.stem + '_SSS_fcst.png')

        title_sst='SST fcst (degC):'+str(name_)
        title_ssh='SSH fcst (m):'+str(name_)
        title_sss='SSS fcst (psu):'+str(name_)

        xyplot(nc.SST[0,:,:].to_masked_array(),grd.geolon,grd.geolat,clim=clim_sst,title=title_sst,save=sst_fig)
        xyplot(nc.SSH[0,:,:].to_masked_array(),grd.geolon,grd.geolat,clim=clim_ssh,title=title_ssh,save=ssh_fig)
        xyplot(nc.SSS[0,:,:].to_masked_array(),grd.geolon,grd.geolat,clim=clim_sss,title=title_sss,save=sss_fig)
        plt.close('all')

    elif (args.run_type == 'incr'):
        nc = xr.open_mfdataset(filename , decode_times=False)
        path_ = Path(filename)
        name_ = Path(filename).name
        if args.figs_path is None:
           sst_fig = str(path_.parent.joinpath(path_.stem + '_SST_incr.png'))
           ssh_fig = str(path_.parent.joinpath(path_.stem + '_SSH_incr.png'))
           sss_fig = str(path_.parent.joinpath(path_.stem + '_SSS_incr.png'))
        else:
           sst_fig = str(args.figs_path+'/'+path_.stem + '_SST_incr.png')
           ssh_fig = str(args.figs_path+'/'+path_.stem + '_SSH_incr.png')
           sss_fig = str(args.figs_path+'/'+path_.stem + '_SSS_incr.png')

        title_sst='SST increment (degC):'+str(name_)
        title_ssh='SSH increment (m):'+str(name_)
        title_sss='SSS increment (psu):'+str(name_)

        temp=nc.temp.where(nc.temp[0,0,:,:] !=0)
        xyplot(temp[0,0,:,:].to_masked_array(),grd.geolon,grd.geolat,clim=clim_sst_incr,title=title_sst,save=sst_fig)
        salt=nc.salt.where(nc.salt[0,0,:,:] !=0)
        xyplot(salt[0,0,:,:].to_masked_array(),grd.geolon,grd.geolat,clim=clim_sss_incr,title=title_sss,save=sss_fig)
        ssh=nc.ssh.where(nc.ssh[0,0,:,:] !=0)
        xyplot(ssh[0,0,:,:].to_masked_array(),grd.geolon,grd.geolat,clim=clim_ssh_incr,title=title_ssh,save=ssh_fig)
        plt.close('all')
    
    else:
        print ("Invalid run_type Argument")
        sys.exit()
