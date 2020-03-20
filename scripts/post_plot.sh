#!/bin/bash -l

echo "post_plot_fcst.sh starts"
echo "CDATE is " $CDATE
cd $RUNCDATE
echo "Location of experiment: "`pwd` 

IceAnlDir=$RUNCDATE/Data
OceanFcstDir=$RUNCDATE/fcst
OceanAnlDir=$RUNCDATE/Data
OceanIncrDir=$RUNCDATE
FiguresDir=$RUNCDATE/Figures

[ ! -d $FiguresDir ] && mkdir -p $FiguresDir

echo "Figures are created at $FiguresDir"

GridFile=$(find $OceanFcstDir -name 'ocn_*.nc' -print -quit)
if [[ -z "$GridFile" ]] ; then
    echo "Grid file containing geolon/geolat does not exist ..."
    exit 1
fi

export QT_QPA_PLATFORM=offscreen
# 1. Plot Ice analysis
files2plot=( "$IceAnlDir"/cic.socagodas.an.*.nc )
if [ -e "${files2plot[0]}" ]; then
    cp -rf $IceAnlDir/cic.socagodas.an.*.nc $OceanFcstDir
    ipython -- $SOCA_EXEC/ice.plot.py                \
           -grid $GridFile                           \
           -data $OceanFcstDir/cic.socagodas.an.*.nc \
           -figs_path $FiguresDir                    \
           -var hice aice
fi

# 2. Plot the ocean fcst 
files2plot=( "$OceanFcstDir"/ocn_*.nc )
if [ -e "${files2plot[0]}" ]; then
    ipython -- $SOCA_EXEC/sfc.plot.py                \
	   -grid $GridFile                           \
	   -data $OceanFcstDir/ocn_*.nc              \
           -run_type fcst                            \
	   -figs_path $FiguresDir 
    # 2a. meridional cross section
    ipython -- $SOCA_EXEC/yz.plot.py                 \
	   -grid $GridFile                           \
	   -data $OceanFcstDir/ocn_*.nc              \
           -run_type fcst                            \
	   -figs_path $FiguresDir
    # 2b. zonal cross section
    ipython -- $SOCA_EXEC/xz.plot.py                 \
	   -grid $GridFile                           \
	   -data $OceanFcstDir/ocn_*.nc              \
           -run_type fcst                            \
	   -figs_path $FiguresDir 
 
fi

# 3. Plot the ocean analysis 
files2plot=( "$OceanAnlDir"/ocn.socagodas.an.*.nc )
if [ -e "${files2plot[0]}" ]; then
    ipython -- $SOCA_EXEC/sfc.plot.py                \
	   -grid $GridFile                           \
	   -data $OceanAnlDir/ocn.socagodas.an.*.nc  \
           -run_type ana                             \
	   -figs_path $FiguresDir 
    # 2a. meridional cross section
#    ipython -- $SOCA_EXEC/yz.plot.py                \
#	   -grid $GridFile                           \
#	   -data $OceanAnlDir/ocn*.nc                \
#           -run_type ana                            \
#	   -figs_path $FiguresDir
    # 2b. zonal cross section
#    ipython -- $SOCA_EXEC/xz.plot.py                \
#	   -grid $GridFile                           \
#	   -data $OceanAnlDir/ocn*.nc                \
#           -run_type ana                            \
#	   -figs_path $FiguresDir 
 
fi


# 4. Plot time averages
[ ! -d $FiguresDir ] && mkdir -p $FiguresDir/time_mean

files2plot=( "$OceanFcstDir"/ocn_*.nc )
if [ -e "${files2plot[0]}" ]; then
    ipython -- $SOCA_EXEC/sfc.time.plot.py           \
           -grid $GridFile                           \
           -data $OceanFcstDir/ocn_*.nc              \
           -figs_path $FiguresDir/time_mean
fi

# 5. Plot the ocean icrement 
files2plot=( "$OceanIncrDir"/incr.1.nc )
if [ -e "${files2plot[0]}" ]; then
    ipython -- $SOCA_EXEC/sfc.plot.py                \
	   -grid $GridFile                           \
	   -data $OceanIncrDir/incr.1.nc             \
           -run_type incr                            \
	   -figs_path $FiguresDir 
fi
